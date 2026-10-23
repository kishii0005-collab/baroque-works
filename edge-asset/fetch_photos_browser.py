"""Fallback for fetch_photos.sh: fetch the photos with a real headless Chromium,
for when Unsplash refuses plain HTTP clients. Writes edge-asset/img/{id}.jpg."""
import os, sys, urllib.request
from playwright.sync_api import sync_playwright

IDS = sys.argv[1:]
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(IMG, exist_ok=True)

def is_jpeg(path):
    return os.path.exists(path) and open(path, 'rb').read(3) == b'\xff\xd8\xff'

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(accept_downloads=True, locale='ja-JP',
                              user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36')
    page = ctx.new_page()
    for pid in IDS:
        out = os.path.join(IMG, f'{pid}.jpg')
        if is_jpeg(out):
            print('skip', pid); continue
        try:
            # 1) photo page -> og:image on the images.unsplash.com CDN
            r = page.goto(f'https://unsplash.com/photos/{pid}', wait_until='domcontentloaded', timeout=45000)
            og = page.eval_on_selector('meta[property="og:image"]', 'm => m.content') if r and r.ok else None
            if og:
                url = og.split('?')[0] + '?w=2000&q=80&fm=jpg&fit=max'
                resp = ctx.request.get(url)
                if resp.ok:
                    open(out, 'wb').write(resp.body())
            # 2) the download link, as a browser download
            if not is_jpeg(out):
                with page.expect_download(timeout=45000) as dl:
                    page.evaluate("u => { const a = document.createElement('a'); a.href = u; document.body.appendChild(a); a.click(); }",
                                  f'https://unsplash.com/photos/{pid}/download?force=true&w=2000')
                dl.value.save_as(out)
            print('ok  ' if is_jpeg(out) else 'fail', pid, '(page status', r.status if r else None, ')')
        except Exception as e:
            print('fail', pid, type(e).__name__, str(e)[:120])
        if not is_jpeg(out) and os.path.exists(out):
            os.remove(out)
    browser.close()
