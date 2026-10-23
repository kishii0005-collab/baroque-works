# breadcrumbs, footer CTA, and the chapter structure of the top page. exec'd from build.py just before pages are written
import json as _json
CRUMB_PARENT={**{f'case-{i}.html':('cases.html','モデルケース') for i in range(1,5)},**{f'column-{i}.html':('column.html','コラム') for i in range(1,7)}}
CRUMB_LABEL={'cases.html':'モデルケース','column.html':'コラム'}
def crumbs(fname,title):
    if fname in ('index.html','404.html'): return ''
    trail=[('index.html','トップ')]
    if fname in CRUMB_PARENT: trail.append(CRUMB_PARENT[fname])
    trail.append((fname,CRUMB_LABEL.get(fname,title)))
    li=''.join((f'<li><a href="{h}">{t}</a></li>' if k<len(trail)-1 else f'<li aria-current="page">{t}</li>') for k,(h,t) in enumerate(trail))
    ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":k+1,"name":t,"item":SITE+('' if h=='index.html' else h)} for k,(h,t) in enumerate(trail)]}
    return f'<nav class="bc" aria-label="パンくずリスト"><ol class="w">{li}</ol></nav><script type="application/ld+json">{_json.dumps(ld,ensure_ascii=False)}</script>'

FOOT_COPY={'service.html':('支援の中身を、|御社の|数字で|ご説明します。','どの支援から始めるかは、会社ごとに違います。現状を伺ったうえで、最初の100日の進め方をご提案します。'),
 'company.html':('代表が、|直接|お話を|伺います。','面談には代表の谷岡が伺います。社外の会議室でも、オンラインでも構いません。'),
 'cases.html':('似た状況でしたら、|そのまま|ご相談ください。','事例と条件が違っていても構いません。会社の状況を伺い、取りうる形をご説明します。'),
 'flow.html':('まずは、|初回面談の|日程だけ|決めませんか。','初回面談で何かを決めていただく必要はありません。1〜2時間、お話を伺うところから始めます。'),
 'partners.html':('案件のご紹介・|ご相談を|お待ちしています。','ノンネーム情報の段階から検討します。5営業日以内に、検討を進めるかどうかをお返事します。')}
for i in range(1,5): FOOT_COPY[f'case-{i}.html']=FOOT_COPY['cases.html']
for i in range(1,7): FOOT_COPY[f'column-{i}.html']=('この記事の内容を、|御社に当てはめると|どうなるか。','個別の状況を伺い、取りうる選択肢と進め方をご説明します。ご相談は無料です。')
def footer_cta(fname):
    if fname in ('contact.html','404.html'): return ''
    h,p=FOOT_COPY.get(fname,('まずは、|話を|聞いてみる|だけで|構いません。','ご相談は無料です。社名を伏せたままでも、決算書がなくても構いません。'))
    return f"""<div class="fcx">
      <div class="fc-t"><p class="fc-en">Contact</p><p class="fc-h">{W(h)}</p>{P(p)}</div>
      <div class="fc-a">
        <a class="fc-b" href="contact.html"{NT}><small>24時間受付・無料</small><span>フォームで相談する</span><i aria-hidden="true"></i></a>
        <a class="fc-b tel" href="tel:0300000000"><small>平日 9:00–18:00</small><span>03-0000-0000</span><i aria-hidden="true"></i></a>
      </div>
    </div>"""

# ---------- top page: five chapters, each opened by a marker, tracked by a side rail ----------
CHAPTERS=[('market','01','課題','いま、工務店に起きていること'),('stance','02','答え','エッジアセットの答え'),('promise','03','約束','引き継ぐときのお約束'),('tcases','04','事例','事例と、ご相談の流れ'),('tseo','05','知る','事業承継を、もっと知る')]
CH_OF={'market':1,'issues':1,'stance':2,'model':2,'tcost':2,'promise':3,'people':3,'cta':3,'tcases':4,'flow':4,'tseo':5,'topfaq':5,'topcol':5,'topnews':5}
def chapterize(html):
    def tag(m):
        cls=m.group(1).split()[0]
        n=CH_OF.get(cls)
        return m.group(0) if not n else m.group(0).replace('<section ',f'<section data-ch="{n}" ',1)
    html=re.sub(r'<section class="([^"]+)"',tag,html)
    for cls,n,short,title in CHAPTERS:
        i=html.find(f'<section data-ch="{int(n)}" class="{cls}')
        if i<0: continue
        j=html.find('<div class="w',i); j=html.find('>',j)+1
        html=html[:j]+f'<p class="chap rv" id="ch{n}"><b>Chapter {n}</b><span>{title}</span></p>'+html[j:]
    rail=''.join(f'<li data-ch="{int(n)}"><a href="#ch{n}"><b>{n}</b><span>{s}</span></a></li>' for c,n,s,t in CHAPTERS)
    return f'<nav class="rail" aria-label="このページの章"><ol>{rail}</ol></nav>'+html
b,d=bodies['index.html']; bodies['index.html']=(chapterize(b),d)

# ---------- menu v3: Japanese first, grouped, current page marked, contact always in view ----------
MENU_MAIN=[('company.html','私たちについて','About','考え方・代表・会社概要'),('service.html','グループの支援','Support','集客・採用・財務・原価の改善'),('cases.html','事例','Cases','4つのモデルケース'),('flow.html','ご相談の流れ','Flow','初回面談から引き継ぎまで')]
MENU_SUB=[('index.html','トップ'),('partners.html','仲介会社・金融機関の方へ'),('column.html','コラム'),('news.html','お知らせ'),('contact.html','お問い合わせ')]
CUR=''
_nav_v2=nav
def nav():
    html=_nav_v2()
    cur=CUR if not CUR.startswith('case-') else 'cases.html'
    cur='column.html' if cur.startswith('column-') else cur
    main=''.join(f'<li><a href="{h}"{NT}{" aria-current=\"page\"" if h==cur else ""}><span class="m3-en">{e}</span><span class="m3-ja">{j}</span><span class="m3-d">{d}</span><i aria-hidden="true"></i></a></li>' for h,j,e,d in MENU_MAIN)
    sub=''.join(f'<li><a href="{h}"{NT}{" aria-current=\"page\"" if h==cur else ""}>{j}</a></li>' for h,j in MENU_SUB)
    inner=f"""<div class="menu-in m3">
    <nav class="m3-l" aria-label="サイトメニュー">
      <p class="m3-k">事業承継をお考えの方へ</p>
      <ul class="m3-main">{main}</ul>
      <ul class="m3-sub">{sub}</ul>
    </nav>
    <div class="m3-r">
      <p class="m3-k">ご相談窓口</p>
      <p class="m3-lead">{W('ご相談は|無料です。|社名を|伏せたままでも|構いません。')}</p>
      <a class="m3-b" href="contact.html"{NT}><small>24時間受付</small><span>フォームで相談する</span><i aria-hidden="true"></i></a>
      <a class="m3-b tel" href="tel:0300000000"><small>平日 9:00–18:00</small><span>03-0000-0000</span><i aria-hidden="true"></i></a>
      <p class="m3-addr">株式会社エッジアセット<br>〒105-0022 東京都港区海岸2丁目5-1-1702</p>
    </div>
  </div>"""
    return re.sub(r'<div class="menu-in">.*?</div>\s*</div>\s*$',inner+'\n</div>',html,flags=re.S)
