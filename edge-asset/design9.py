# PASS 9 (2026-11-15): more photos and ornaments on the top page. Runs after polish.py, edits the finished bodies.
import re
def _sub_once(html, old, new, label):
    assert old in html, f'design9: {label} not found'
    return html.replace(old, new, 1)

b, d = bodies['index.html']

# promise: a photo under the heading column
i = b.index('class="promise"'); j = b.index('</header>', i)
b = b[:j] + f'<figure class="pr-fig rv"><div class="ph">{img("ai-interior","完成した木造住宅のリビング",1200)}</div><figcaption>引き渡した家と、その後の三十年を守る。</figcaption></figure>' + b[j:]

# world: a wide photo band above the succession chain
b = _sub_once(b, '<div class="wd-chain rv"', f'<figure class="wd-band rv"><div class="ph">{img("ai-town","丘から見た地方都市の住宅地",2000)}</div><figcaption><span>Our field</span>地域の住宅会社が、まちの家を守り続ける。</figcaption></figure><div class="wd-chain rv"', 'world chain')

# people: a photo on each card
pics = [('ai-office','打ち合わせスペース'),('ai-tools','大工道具'),('ai-interior','完成した住まい'),('ai-wood','刻んだ構造材')]
i = b.index('<div class="pg">'); j = b.index('</div>', i)
seg = b[i:j]; k = iter(pics)
seg = re.sub(r'<article class="rv">', lambda m: '<article class="rv">' + (lambda p: f'<div class="ph pc-ph">{img(p[0],p[1],800)}</div>')(next(k)), seg)
b = b[:i] + seg + b[j:]

# cta: dusk photo
i = b.index('class="cta"'); j = b.index('<div class="ph">', i); k2 = b.index('</div>', j)
b = b[:j] + f'<div class="ph">{img("ai-dusk","",2000)}</div>' + b[k2 + 6:]

bodies['index.html'] = (b, d)

# ---- sub-pages: a full-width photo band before the closing section, on pages that had no photo between text blocks
def pband(pid, alt, en, cap):
    return f'<section class="pband"><figure class="wd-band rv"><div class="ph">{img(pid, alt, 2000)}</div><figcaption><span>{en}</span>{cap}</figcaption></figure></section>'
BANDS = {
  'partners.html': ('<section class="nextp"', 'ai-plan', '机に広げた住宅の図面', 'For partners', '案件のご紹介を、地域の住宅会社の次の三十年につなげます。'),
  'faq.html':      ('<section class="nextp"', 'ai-interior', '完成した木造住宅のリビング', 'Ask us', 'ここにない疑問も、まずはお気軽にお尋ねください。'),
  'news.html':     ('<section class="nextp"', 'ai-town', '丘から見た地方都市の住宅地', 'News', '地域の住宅会社とともに、一社ずつ歩んでいます。'),
  'valuation.html':('<section class="nextp"', 'ai-wood', '刻みを入れた杉・檜の構造材', 'Beyond numbers', '数字の先にある、会社の中身まで見て判断します。'),
  'contact.html':  ('<section class="faq"', 'ai-dusk', '夕暮れに明かりが灯る木造住宅', 'Contact', '社名を伏せたままでも、話を聞いてみるだけでも構いません。'),
  'case-3.html':   ('<section class="nextp"', 'ai-house', '庭木に囲まれた木造住宅', 'Model case', '施主様との約束を、次の世代へ。'),
  'case-4.html':   ('<section class="nextp"', 'ai-renov', '床を張り替えている改修中の室内', 'Model case', '利益が残る仕組みに、一つずつ直していく。'),
  'case-5.html':   ('<section class="nextp"', 'ai-tools', '作業台に置かれた大工道具', 'Model case', '腕と信頼を、三代目へ。'),
}
for f, (marker, pid, alt, en, cap) in BANDS.items():
    if f not in bodies: continue
    bb, dd = bodies[f]
    if marker in bb: bodies[f] = (bb.replace(marker, pband(pid, alt, en, cap) + marker, 1), dd)
# second band on the long pages
for f, marker, pid, alt, en, cap in [
  ('company.html', '<section class="compare"', 'ai-town', '丘から見た地方都市の住宅地', 'Our way', '売らずに、長く。地域の会社として続けていく。'),
  ('company.html', '<section class="hist"', 'ai-wood', '刻みを入れた杉・檜の構造材', 'History', '一社ずつ、時間をかけて積み上げてきました。'),
  ('service.html', '<section class="d100"', 'ai-office', '無垢材のテーブルがある打ち合わせスペース', 'First 100 days', '引き継ぎの最初の百日を、一緒に設計します。'),
  ('flow.html',    '<section class="think"', 'ai-plan', '机に広げた住宅の図面', 'Before you decide', '決める前に、考えておくと良いこと。')]:
    bb, dd = bodies[f]
    if marker in bb: bodies[f] = (bb.replace(marker, pband(pid, alt, en, cap) + marker, 1), dd)

# ---- PASS 10 (2026-11-16): top FAQ gets a photo under the left heading column
b, d = bodies['index.html']
b = _sub_once(b, '<a class="tl" href="faq.html">', f'<figure class="tf-fig"><div class="ph">{img("ai-key","",900)}</div></figure><a class="tl" href="faq.html">', 'topfaq link')
bodies['index.html'] = (b, d)
