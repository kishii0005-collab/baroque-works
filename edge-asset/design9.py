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
