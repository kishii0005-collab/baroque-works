# Ungallery 来場予約ページ／イベントページ

| ファイル | 用途 |
|---|---|
| `reserve.html` | 常設：勝目町モデルハウスの来場予約ページ |
| `event.html` | イベントLP：住まいづくりフェア（日程枠を選んで予約） |

ブラウザで開くとそのまま確認できる（フォーム送信はプレビュー用のダミー動作）。

## 公開前に必ず差し替えるもの

1. **`【要確認】` の箇所すべて**：定休日、駐車場台数、特典内容、イベント日程、各回の組数
2. **`PHOTO ／ ...` のグレーの枠**：実際の写真に差し替える（`<div class="ph">` を `<img src="..." alt="...">` に置換）
3. **イベントの日程ボタン**（`event.html` の `#ugSlots`）：日付・時間。満席の枠は `class="is-full" disabled` を付ける
4. **トンマナの最終確認**：本サイトのCSSを取得できなかったため、色・書体は推定値。`.ug{ --bg … }` の先頭にある色の変数だけ変えれば全体に反映される

## WordPressへの設置手順（固定ページ）

> 貼り付け用ファイルは `wp/` に番号順で用意済み（1_追加CSS → 2_CF7フォーム → 3_本文 …）。以下はその元になる説明。


1. 固定ページを新規作成（スラッグ例：`reserve`／`event-fair`）
2. テンプレートは**ヘッダー・フッターあり／サイドバーなし（1カラム・全幅）**を選ぶ
3. `<style>…</style>` の中身 → 「外観 › カスタマイズ › 追加CSS」に貼る（`.ug` 内に閉じているので既存デザインを崩さない）
   - `body{...}` の1行は削除してよい
   - Google Fonts の `<link>` は、テーマ側で読み込めない場合のみ `functions.php` に追加
4. `<div class="ug">` 〜 `</div>`（`<script>` の手前まで）を「カスタムHTML」ブロックに貼る
5. `<form id="ugForm">…</form>` を下記の Contact Form 7 ショートコードに置き換える
6. `event.html` の `<script>` は**日程ボタンの部分だけ**残す（送信処理の部分は削除）。CF7の日時入力欄IDを `slot` にしておくこと
7. フッター固定ボタン（`.sticky`）がテーマ側の固定バーと重なる場合は片方を消す

## Contact Form 7 用フォームコード

### 来場予約（reserve）

```
<div class="row"><label>第1希望日<span class="req">必須</span></label><div class="pair">[date* date1 min:today+1days] [select* time1 first_as_label "時間を選択" "10:00〜" "11:00〜" "13:00〜" "14:00〜" "15:00〜" "16:00〜"]</div></div>
<div class="row"><label>第2希望日<span class="opt">任意</span></label><div class="pair">[date date2 min:today+1days] [select time2 first_as_label "時間を選択" "10:00〜" "11:00〜" "13:00〜" "14:00〜" "15:00〜" "16:00〜"]</div></div>
<div class="row"><div class="lbl">ご来場人数<span class="req">必須</span></div><div class="pair"><div><small>大人</small>[select* adult "1名" "2名" "3名" "4名以上"]</div><div><small>お子さま</small>[select child "0名" "1名" "2名" "3名以上"]</div></div></div>
<div class="row"><label>お名前<span class="req">必須</span></label>[text* your-name placeholder "例）山田 太郎"]</div>
<div class="row"><label>ふりがな<span class="req">必須</span></label>[text* kana placeholder "例）やまだ たろう"]</div>
<div class="row"><label>電話番号<span class="req">必須</span></label>[tel* tel placeholder "例）090-1234-5678"]</div>
<div class="row"><label>メールアドレス<span class="req">必須</span></label>[email* your-email placeholder "例）info@example.com"]</div>
<div class="row"><label>お住まいの地域<span class="opt">任意</span></label>[select area first_as_label "選択してください" "薩摩川内市" "鹿児島市" "姶良市" "霧島市" "いちき串木野市" "出水市" "阿久根市" "さつま町" "その他"]</div>
<div class="row"><div class="lbl">土地について<span class="opt">任意</span></div><div class="chips">[radio land use_label_element "土地あり" "土地探し中" "建て替え" "まだ未定"]</div></div>
<div class="row"><div class="lbl">建築予定時期<span class="opt">任意</span></div><div class="chips">[radio when use_label_element "半年以内" "1年以内" "2年以内" "未定"]</div></div>
<div class="row"><div class="lbl">ご相談したいこと<span class="opt">複数可</span></div><div class="chips">[checkbox topic use_label_element "デザイン・間取り" "資金計画・住宅ローン" "土地探し" "性能・断熱" "まずは見学だけ"]</div></div>
<div class="row"><label>当社を知ったきっかけ<span class="opt">任意</span></label>[select source first_as_label "選択してください" "Instagram" "Google検索" "Googleマップ" "チラシ" "知人の紹介" "通りがかり" "その他"]</div>
<div class="row"><label>ご質問・ご要望<span class="opt">任意</span></label>[textarea message]</div>
<div class="agree">[acceptance privacy] <a href="/privacy/" target="_blank">個人情報の取り扱い</a>に同意する [/acceptance]</div>
<div class="submit">[submit class:btn "内容を確認して予約する"]</div>
```

### イベント（event）

```
<div class="row"><label>ご希望日時<span class="req">必須</span></label>[text* slot id:slot readonly placeholder "上の日程から選択してください"]</div>
（以下、人数・お名前・電話・メール・土地・相談内容・備考・同意・送信は reserve と同じ）
```

> CF7のラジオ/チェックボックスは `<span class="wpcf7-list-item"><label><input><span class="wpcf7-list-item-label">` という構造になるため、チップ表示を効かせるには追加CSSに次を足す：
>
> ```css
> .ug .chips .wpcf7-list-item{margin:0}
> .ug .chips .wpcf7-list-item-label{display:inline-block;padding:8px 18px;border:1px solid var(--line);font-size:13px;background:var(--bg);cursor:pointer}
> .ug .chips input:checked + .wpcf7-list-item-label{background:var(--char);border-color:var(--char);color:#fff}
> ```

## 計測（入れないと広告の最適化ができない）

- 送信完了を **サンクスページ（`/reserve/thanks/`）へのリダイレクト** にし、GA4のキーイベント＋Metaピクセルの `Lead` / `Schedule` をそこで発火させる
- 予約フォームとイベントフォームは**別のコンバージョン**として計測（どちらの導線が効いているか分けて見るため）
- 「知ったきっかけ」は広告媒体の自己申告データとして月次で集計する
