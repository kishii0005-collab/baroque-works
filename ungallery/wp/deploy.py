#!/usr/bin/env python3
"""Ungallery 来場予約／イベントページを WordPress REST API で一括作成する。

すべて「下書き」で作成する（公開は管理画面でプレビュー確認後に手動）。
何度実行しても、同じスラッグ・同じフォーム名があれば上書き更新する。

必要な環境変数:
  WP_URL           任意。サイトのトップURL（省略時 https://ungallery.jp）
  WP_USER          WordPressのユーザー名
  WP_APP_PASSWORD  ユーザー › プロフィール › アプリケーションパスワード で発行したもの
  WP_NOTIFY_TO     任意。予約通知の送信先（省略時はサイト管理者メール）

使い方:
  python3 deploy.py --dry-run   # 送信内容の確認のみ
  python3 deploy.py             # 実行
"""
import base64
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
DRY = "--dry-run" in sys.argv

PAGES = [
    # slug, title, body file, CF7 form file, form title, mail subject, mail body key
    dict(slug="reserve", title="来場予約", body="3_来場予約_本文.html",
         form="2_CF7フォーム_来場予約.txt", form_title="来場予約",
         subject="【来場予約】[your-name] 様（[date1] [time1]）", kind="reserve"),
    dict(slug="event-fair", title="住まいづくりフェア", body="5_イベント_本文.html",
         form="4_CF7フォーム_イベント.txt", form_title="イベント予約",
         subject="【フェア予約】[your-name] 様（[slot]）", kind="event"),
]

MAIL_BODY = {
    "reserve": """お名前：[your-name]（[kana]）
電話：[tel]
メール：[your-email]
第1希望：[date1] [time1]
第2希望：[date2] [time2]
人数：大人[adult]／子ども[child]
地域：[area]
土地：[land]
時期：[when]
相談内容：[topic]
きっかけ：[source]
備考：[message]""",
    "event": """お名前：[your-name]
電話：[tel]
メール：[your-email]
希望日時：[slot]
人数：大人[adult]／子ども[child]
土地：[land]
相談内容：[topic]
備考：[message]""",
}

REPLY = """[your-name] 様

この度はUngalleryへご予約いただき、ありがとうございます。
以下の内容で受け付けました。担当者より2営業日以内に、日時確定のご連絡をいたします。

ご希望日時：{when}
ご来場人数：大人[adult]／お子さま[child]

会場：勝目町モデルハウス（鹿児島県薩摩川内市勝目町5115-5）
お問い合わせ：0996-41-3938（10:00〜17:00）

当日お会いできることを楽しみにしております。
Ungallery"""

THANKS = """<!-- wp:html -->
<div class="ug"><section><div class="narrow" style="text-align:center">
<div class="ttl"><span class="en">Thank you</span><h2>ご予約を受け付けました</h2></div>
<p>ご入力いただいたメールアドレスに、確認メールをお送りしました。<br>担当者より2営業日以内に、日時確定のご連絡をいたします。</p>
<p class="note">※確認メールが届かない場合は、お手数ですが 0996-41-3938 までお電話ください。</p>
<p style="margin-top:40px"><a class="btn ghost" href="/">トップへ戻る</a></p>
</div></section></div>
<!-- /wp:html -->"""


def env(name, default=None):
    v = os.environ.get(name, default)
    if v is None and not DRY:
        sys.exit(f"環境変数 {name} が設定されていません")
    return v


BASE = (os.environ.get("WP_URL") or "https://ungallery.jp").rstrip("/")
AUTH = base64.b64encode(
    f"{env('WP_USER', 'dry')}:{(env('WP_APP_PASSWORD', 'dry') or '').replace(' ', '')}".encode()
).decode()
DOMAIN = urllib.parse.urlparse(BASE).hostname or "ungallery.jp"
NOTIFY = os.environ.get("WP_NOTIFY_TO") or "[_site_admin_email]"


def api(method, path, data=None, query=None):
    # パーマリンク設定やWP本体の設置ディレクトリ(/cms)に左右されない ?rest_route= 形式で呼ぶ
    url = f"{BASE}/?" + urllib.parse.urlencode({"rest_route": "/" + path, **(query or {})})
    if DRY and method != "GET":
        print(f"[dry-run] {method} {url}")
        if data:
            print("  " + json.dumps({k: (v[:80] + "…" if isinstance(v, str) and len(v) > 80 else v)
                                     for k, v in data.items()}, ensure_ascii=False)[:600])
        return {"id": 0}
    if DRY:
        return []
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Basic {AUTH}",
        "Content-Type": "application/json",
        "User-Agent": "ungallery-deploy/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:500]
        hint = ""
        if e.code in (401, 403):
            hint = ("\n→ 認証エラー。ユーザー名／アプリケーションパスワード、"
                    "またはセキュリティプラグイン（CloudSecure WP Security）のREST API制限を確認してください。")
        if e.code == 404 and "contact-form-7" in path:
            hint = "\n→ Contact Form 7 のREST APIが見つかりません。CF7が有効か確認してください。"
        sys.exit(f"{method} {url} → HTTP {e.code}\n{msg}{hint}")


def read(name):
    return (HERE / name).read_text(encoding="utf-8")


def upsert_form(p):
    title = p["form_title"]
    found = api("GET", "contact-form-7/v1/contact-forms", query={"search": title, "per_page": 50})
    existing = next((f for f in (found or []) if f.get("title") == title), None)
    when = "[slot]" if p["kind"] == "event" else "[date1] [time1]"
    payload = {
        "title": title,
        "locale": "ja",
        "form": read(p["form"]),
        "mail": {
            "subject": p["subject"],
            "sender": f"Ungallery <wordpress@{DOMAIN}>",
            "recipient": NOTIFY,
            "body": MAIL_BODY[p["kind"]],
            "additional_headers": "Reply-To: [your-email]",
            "attachments": "", "use_html": False, "exclude_blank": False,
        },
        "mail_2": {
            "active": True,
            "subject": "【Ungallery】ご予約を受け付けました",
            "sender": f"Ungallery <wordpress@{DOMAIN}>",
            "recipient": "[your-email]",
            "body": REPLY.format(when=when),
            "additional_headers": f"Reply-To: {NOTIFY}" if "@" in NOTIFY and "[" not in NOTIFY else "",
            "attachments": "", "use_html": False, "exclude_blank": False,
        },
    }
    if existing:
        res = api("POST", f"contact-form-7/v1/contact-forms/{existing['id']}", payload)
        fid = existing["id"]
        print(f"フォーム更新: {title} (id={fid})")
    else:
        res = api("POST", "contact-form-7/v1/contact-forms", payload)
        fid = res.get("id")
        print(f"フォーム作成: {title} (id={fid})")
    errs = (res or {}).get("config_errors") if isinstance(res, dict) else None
    if errs:
        print(f"  ⚠ CF7の設定警告: {json.dumps(errs, ensure_ascii=False)[:300]}")
    return fid


def find_page(slug, parent=None):
    q = {"slug": slug, "status": "publish,draft,pending,private", "context": "edit"}
    if parent is not None:
        q["parent"] = parent
    found = api("GET", "wp/v2/pages", query=q)
    return found[0] if found else None


def upsert_page(slug, title, content, parent=0):
    existing = find_page(slug, parent if parent else None)
    data = {"title": title, "slug": slug, "content": content, "parent": parent}
    if existing:
        api("POST", f"wp/v2/pages/{existing['id']}", data)  # ステータスは触らない（公開済みなら公開のまま）
        print(f"ページ更新: /{slug}/ (id={existing['id']}, status={existing.get('status')})")
        return existing["id"]
    data["status"] = "draft"
    res = api("POST", "wp/v2/pages", data)
    print(f"ページ作成(下書き): {title} → /{slug}/ (id={res.get('id')})")
    return res.get("id")


def main():
    css = read("1_追加CSS.css")
    # テーマのwpautopで <p> が挟まらないよう、style は1行に圧縮して本文内に同梱
    css_inline = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css_inline = re.sub(r"\s*\n\s*", "", css_inline)
    for p in PAGES:
        fid = upsert_form(p)
        body = read(p["body"])
        body = re.sub(r'\[contact-form-7 id="[^"]*"', f'[contact-form-7 id="{fid}"', body)
        content = f"<!-- wp:html -->\n<style>{css_inline}</style>\n{body}\n<!-- /wp:html -->"
        pid = upsert_page(p["slug"], p["title"], content)
        upsert_page("thanks", "ご予約ありがとうございます",
                    f"<!-- wp:html -->\n<style>{css_inline}</style>\n<!-- /wp:html -->\n{THANKS}", parent=pid)
    print("\n完了。管理画面 › 固定ページ で下書きをプレビューし、確認後に「公開」してください。")
    print("  https://ungallery.jp/cms/wp-admin/edit.php?post_type=page")


if __name__ == "__main__":
    main()
