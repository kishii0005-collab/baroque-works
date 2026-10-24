# breadcrumbs, footer CTA, and the chapter structure of the top page. exec'd from build.py just before pages are written
import json as _json
CRUMB_PARENT={**{f'case-{i}.html':('cases.html','事例') for i in range(1,5)},**{f'column-{i}.html':('column.html','コラム') for i in range(1,7)}}
CRUMB_LABEL={'cases.html':'事例','column.html':'コラム'}
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
MENU_SUB=[('index.html','トップ'),('partners.html','仲介会社・金融機関の方へ'),('column.html','コラム'),('faq.html','よくあるご質問'),('news.html','お知らせ'),('contact.html','お問い合わせ')]
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

# ---------- structure pass 2: FAQ page, representative teaser on the top page, sitemap page ----------
import html as _html
FAQ_CATS=[
 ('consult','ご相談について',[faqs[0],faqs[3],
   ('相談に費用はかかりますか。','かかりません。初回面談から最終契約まで、私たちから社長に費用をご請求することはありません。'),
   ('検討の結果、お断りされることはありますか。','あります。お引き受けできない場合も、その理由と、ほかに取りうる選択肢をお伝えします。ご相談の事実や拝見した資料を外部に出すことはありません。'),
   ('決算書がないと相談できませんか。','初回面談に決算書は不要です。会社の規模や状況を、話せる範囲で伺うところから始めます。')]),
 ('terms','引き継ぎの条件',[faqs[2],
   ('譲渡代金は、いつ、どのように支払われますか。','株式譲渡契約で定めた代金を、原則としてクロージング（最終契約）時にお支払いします。分割など個別の条件はご相談ください。'),
   ('社長個人の借入の保証はどうなりますか。','借入に付いている社長個人の保証は、金融機関と協議のうえ、クロージング時点での解除を目指します。'),
   faqs[5],
   ('株式の一部を持ち続けることはできますか。','できます。社長を続けながら一部の株式を持ち続ける形も、事例としてご紹介しています。ご希望をふまえて設計します。'),
   faqs[6]]),
 ('people','社員・施主様・取引先',[faqs[1],
   ('引き渡した家の保証や定期点検は、どうなりますか。','株式譲渡では会社そのものが変わらないため、保証も定期点検も会社に残ります。原則として、これまでの担当者が続けます。'),
   faqs[4],SVCFAQ_Q[0],SVCFAQ_Q[2]]),
 ('after','グループ入りのあと',[SVCFAQ_Q[1],SVCFAQ_Q[3],SVCFAQ_Q[4],
   ('最初の100日で、何が変わりますか。','初日に社長と私たちで社員の皆さまにご説明し、30日で月次の数字の締め方を、100日で採用と原価の仕組みを整えます。現場の仕事と施主様との関係は変えません。')]),
 ('partners','仲介会社・金融機関の方',PFAQ_Q),
]
def _plain(t): return re.sub(r'<[^>]+>','',t)
FAQ_LD={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":_plain(a)}} for _,_,qs in FAQ_CATS for q,a in qs]}
def faq_page():
    navi=''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t,_ in FAQ_CATS)
    cats=''.join(f'<div class="fq-cat" id="{i}"><div class="fq-h"><p class="fq-n">{k+1:02d}</p><h2>{t}</h2></div><div class="fq-l">'+''.join(f'<details><summary><span class="q">Q.</span><span>{nb(q,6)}</span><span class="pm"></span></summary><div class="a"><span>A.</span>{P(a)}</div></details>' for q,a in qs)+'</div></div>' for k,(i,t,qs) in enumerate(FAQ_CATS))
    return (phero('FAQ','よくあるご質問','ご相談の前に、社長や仲介会社の方からよく伺う質問をまとめました。ここにない質問は、お問い合わせからお寄せください。','Q6sCJFHCubc')
      +f'<section class="faqp"><div class="w"><ul class="fq-nav">{navi}</ul>{cats}<p class="fq-more">{nb("ここにない質問は、お問い合わせフォームか電話でお寄せください。2営業日以内にお答えします。")}</p></div></section>'
      +'<script type="application/ld+json">'+_json.dumps(FAQ_LD,ensure_ascii=False)+'</script>'
      +nextlink('contact.html','Contact','ご相談・お問い合わせ'))
PAGES.append(('faq.html','よくあるご質問'))
bodies['faq.html']=(faq_page(),'工務店・住宅会社の事業承継についてよくあるご質問。ご相談、引き継ぎの条件、社員・施主様・取引先、グループ入り後、仲介会社の方へ。')

SM_GROUPS=[('会社を知る',[('index.html','トップ'),('company.html','私たちについて'),('company.html#message','代表メッセージ'),('company.html#profile','代表プロフィール'),('company.html#company','会社概要')]),
 ('事業承継のご相談',[('service.html','グループの支援'),('service.html#cost','原価の改善'),('cases.html','事例'),('flow.html','ご相談の流れ'),('faq.html','よくあるご質問'),('contact.html','ご相談・お問い合わせ')]),
 ('仲介会社・金融機関の方へ',[('partners.html','ご紹介のご案内')]),
 ('読む',[('column.html','コラム')]+[(a['slug'],a['title']) for a in ARTICLES]+[('news.html','お知らせ')]),
 ('サイトについて',[('privacy.html','プライバシーポリシー'),('terms.html','サイトのご利用について')])]
def sitemap_page():
    g=''.join(f'<div class="sm-g"><h2>{t}</h2><ul>'+''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in ls)+'</ul></div>' for t,ls in SM_GROUPS)
    return phero('Sitemap','サイトマップ','','4mEyvORkbN0')+f'<section class="smap"><div class="w"><div class="sm-grid">{g}</div></div></section>'
PAGES.append(('sitemap.html','サイトマップ'))
bodies['sitemap.html']=(sitemap_page(),'株式会社エッジアセットのサイトマップ。')

TOPMSG=f"""<section class="tmsg">
  <div class="w">
    <div class="tm-ph"><div class="ph">{img('rD28m9BmXVs','代表写真（撮影予定）',1000)}</div><span class="tm-cap">代表写真は撮影予定</span></div>
    <div class="tm-tx rv">
      <p class="sh-ja">代表メッセージ</p>
      <h2>{W('会社を|売る、|という|言葉に|抵抗がある方へ。')}</h2>
      {P('大手に売れば、名前は数年で消えるかもしれない。ファンドに売れば、数年後にまた別の誰かに売られるかもしれない。その不安に正面から答えるために、この会社をつくりました。')}
      <div class="tm-who"><b>谷岡 佑亮</b><span>株式会社エッジアセット 代表取締役</span><small>船井総合研究所にて、上位0.5%の年間粗利獲得実績を複数年。経営再建・成長戦略の実行支援を経て、建築業界の採用・営業・業務改善を支援。</small></div>
      <a class="btn btn-navy" href="company.html#message"{NT}>メッセージの全文を読む {AR}</a>
    </div>
  </div>
</section>"""
CH_OF['tmsg']=3
b,d=bodies['index.html']
_cta='<section data-ch="3" class="cta">'
assert _cta in b
bodies['index.html']=(b.replace(_cta,TOPMSG.replace('<section ','<section data-ch="3" ',1)+_cta,1),d)
