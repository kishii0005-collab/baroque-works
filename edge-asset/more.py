# ===== expanded content + new hero (exec'd from build.py after the base sections) =====
FV_SLIDES=[('GpJ9p1QH7O4','大阪の夜景'),('q1tyQip5AQQ','大阪の住宅の外観'),('a8A-z_ZPEC0','横浜の建築'),('rD28m9BmXVs','東京のビル街')]
fv_s=''.join(f'<div class="slide ph{" on" if i==0 else ""}">{img(pid,alt,2400,i>0)}</div>' for i,(pid,alt) in enumerate(FV_SLIDES))
def split_chars(t):
    out=[];k=0
    for seg in t.split('|'):
        out.append('<span class="wd">'+''.join(f'<span class="ch" style="--d:{(k:=k+1)*0.035:.3f}s">{c}</span>' for c in seg)+'</span>')
    return ''.join(out)
FV=f"""<section class="hx" aria-label="メインビジュアル">
  <div class="hx-slides">{fv_s}</div>
  <div class="hx-grid" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="hx-in">
    <p class="hx-kick"><span>01</span>BUSINESS SUCCESSION PLATFORM</p>
    <h1 class="hx-h">{split_chars('地域の|工務店を、|つぎの|三十年へ。')}</h1>
    {P('後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営する。社名も、社員も、施主様へのアフターのお約束も、そのまま次の世代へつなぎます。','hx-lead')}
    <div class="hx-act"><a class="btn btn-white" href="contact.html">事業承継について相談する {AR}</a><a class="tl hx-tl" href="partners.html">仲介会社・金融機関の方へ {AR}</a></div>
  </div>
  <div class="hx-foot">
    <div class="hx-pager"><span id="cnt">01</span><span class="pager" id="pager"></span><span>04</span></div>
    <a class="hx-news" href="news.html"><b>NEWS</b><time datetime="2026-10-22">2026.10.22</time><span>コーポレートサイトを公開しました</span></a>
    <span class="hx-scroll">SCROLL</span>
  </div>
  <div class="hx-marq" aria-hidden="true"><span>EDGE ASSET — BUSINESS SUCCESSION FOR JAPANESE HOME BUILDERS — LONG-TERM OWNERSHIP — </span><span>EDGE ASSET — BUSINESS SUCCESSION FOR JAPANESE HOME BUILDERS — LONG-TERM OWNERSHIP — </span></div>
</section>"""

ISSUES=f"""<section class="issues">
  <div class="w">
    {head('Issues','住宅会社が直面する課題','黒字でも、|続けられない|理由が|あります','地域の工務店が会社をたたむ理由は、業績だけではありません。私たちは、次の三つの課題をまとめて引き受けます。')}
    <div class="is3">
      <article class="rv"><p class="n">01</p><h3>{W('継ぐ人が|いない')}</h3>{P('建設業の後継者不在率は57.3%と、業種別で最も高い水準です。子どもが別の道へ進み、社員に継がせるには株式を買い取る資金が足りない。多くの社長が同じ壁に当たっています。')}</article>
      <article class="rv"><p class="n">02</p><h3>{W('人が|採れない')}</h3>{P('設計・現場監督・大工の採用は、規模の小さい会社ほど不利です。求人を出しても応募が来ず、受注があっても棟数を増やせない状況が続きます。')}</article>
      <article class="rv"><p class="n">03</p><h3>{W('社長に|仕事が|集中する')}</h3>{P('集客、見積、資金繰り、労務、法改正への対応。家づくり以外の仕事がすべて社長に集まり、本来の強みである現場と施主様に時間を割けなくなっています。')}</article>
    </div>
  </div>
</section>"""

MODEL=f"""<section class="model dark" id="model">
  <div class="w">
    {head('Group model','グループの仕組み','各社の|看板は|そのまま。|裏側の仕事を|グループで|共有します','エッジアセットはグループの本部として、各社に共通する仕事を引き受けます。家づくりと施主様との関係は、これまでどおり各社が担います。')}
    <div class="md rv" role="img" aria-label="エッジアセットが本部として集客・採用・財務・仕入・システム・人材を担い、各社は社名と現場をそのまま残す仕組みの図">
      <div class="md-hq"><p class="k">HEADQUARTERS</p><p class="t">エッジアセット</p><p class="s">グループ本部</p></div>
      <ul class="md-fn"><li>集客</li><li>採用</li><li>財務・資金</li><li>仕入</li><li>システム</li><li>人材育成</li></ul>
      <div class="md-co">
        <div><p class="t">A社</p><p class="s">社名・ブランド継続</p></div>
        <div><p class="t">B社</p><p class="s">社名・ブランド継続</p></div>
        <div><p class="t">C社</p><p class="s">社名・ブランド継続</p></div>
      </div>
      <p class="md-note">各社が担うこと：設計・施工・施主様との打ち合わせ・アフター対応・地域での営業</p>
    </div>
  </div>
</section>"""

DAYS=[('Day 1','社員の皆さまへのご説明','社長と私たちが一緒に、グループ入りの理由と、変わらないことを直接お伝えします。'),
      ('30 days','数字の見える化','月次決算の仕組みを整え、受注・原価・資金繰りを毎月一緒に確認できる状態にします。'),
      ('60 days','集客と採用の立て直し','広告・Webの反響を計測し始め、グループ合同の求人を出します。'),
      ('100 days','中期計画の策定','3年後の会社の姿を社長・幹部と一緒に描き、次の社長候補の育成計画を決めます。')]
D100=f"""<section class="d100">
  <div class="w">
    {head('First 100 days','グループ入り後の100日','最初の|100日で、|ここまで|進めます','急に何かを変えることはしません。現場の負担にならない順番で、少しずつ仕組みを整えます。')}
    <ol class="dl">{''.join(f'<li class="rv"><p class="day">{d}</p><h3>{W(h)}</h3>{P(t)}</li>' for d,h,t in DAYS)}</ol>
  </div>
</section>"""

BA=[('経理・決算','社長が夜に帳簿をつけ、決算は年1回','本部が月次決算を締め、翌月10日に数字を共有'),
    ('集客','紹介と見学会頼みで、反響が読めない','広告・Web・Googleマップの反響を毎月計測'),
    ('採用','自社だけで求人を出し、応募が少ない','グループ合同で新卒・中途を採用し、研修も共通化'),
    ('仕入','会社ごとに建材・設備を発注','グループの発注量をまとめて単価を交渉'),
    ('事業承継','後継者が決まらず、社長の個人保証も残る','次期社長を計画的に育て、個人保証の解除に取り組む')]
BEFORE=f"""<section class="ba">
  <div class="w">
    {head('Before / After','グループ入りで変わること','変わるのは、|社長の|手元の|仕事です')}
    <div class="tbl rv"><table class="batbl"><thead><tr><th>領域</th><th>グループ入り前</th><th class="af">グループ入り後</th></tr></thead><tbody>{''.join(f'<tr><th>{a}</th><td>{b}</td><td class="af">{c}</td></tr>' for a,b,c in BA)}</tbody></table></div>
  </div>
</section>"""

TOPFAQ_Q=[('相談したことが、社員や取引先に知られることはありませんか。','ありません。面談は社外かオンラインで行い、秘密保持契約は初回面談の段階から結べます。'),
          ('赤字の会社でも相談できますか。','はい。赤字の理由と改善の見通しを一緒に整理するところから始めます。'),
          ('社長は辞めなければいけませんか。','いいえ。引き継ぎ期間だけ残る形も、社長を続ける形も選べます。')]
TOPFAQ=f"""<section class="topfaq">
  <div class="w tf">
    <div>{head('FAQ','よくあるご質問','')}<a class="tl" href="contact.html#faq">すべての質問を見る {AR}</a></div>
    <div>{''.join(f'<details><summary><span class="q">Q.</span><span>{nb(q,6)}</span><span class="pm"></span></summary><div class="a"><span>A.</span>{P(a)}</div></details>' for q,a in TOPFAQ_Q)}</div>
  </div>
</section>""".replace('<h2></h2>','')

VMV=f"""<section class="vmv">
  <div class="w">
    {head('Vision / Mission / Value','私たちが目指すもの','地域の|住まいを|守り続ける|会社を、|全国に。')}
    <div class="vm2">
      <div class="rv"><p class="k">VISION</p><h3>{W('地域の|住まいを|守り続ける|会社を、|全国に。')}</h3>{P('家を建てた会社が、三十年後もその家の点検に伺える。そんな当たり前を、後継者がいない工務店にも続けられるようにします。')}</div>
      <div class="rv"><p class="k">MISSION</p><h3>{W('工務店の|事業承継を、|廃業以外の|選択肢に。')}</h3>{P('継ぐ人がいないという理由で、黒字の会社が消えることをなくします。社名と雇用を残したまま引き継ぐ受け皿を、住宅業界につくります。')}</div>
    </div>
    <ul class="val">{''.join(f'<li class="rv"><p class="n">{i+1:02d}</p><h4>{W(h)}</h4>{P(t)}</li>' for i,(h,t) in enumerate([('売らない','買った会社を手放して利益を得ることを前提にしません。'),('現場に口を出さない','家づくりの方針は、各社の大工と設計者が決めます。'),('数字は毎月、一緒に見る','感覚ではなく月次の数字で、社長と同じ景色を見ます。'),('約束は契約書に書く','口約束ではなく、守ることを条項として残します。')]))}</ul>
  </div>
</section>"""

GOV=f"""<section class="gov">
  <div class="w g2">
    <div class="rv">{head('Governance','グループ経営の考え方','任せる|範囲と、|一緒に|決める|範囲')}</div>
    <div class="rv"><table class="govtbl"><thead><tr><th>判断すること</th><th>決める人</th></tr></thead><tbody>
      <tr><td>設計・仕様・施工方法</td><td>各社</td></tr>
      <tr><td>個別案件の見積と受注</td><td>各社</td></tr>
      <tr><td>採用（配属・現場の育成）</td><td>各社</td></tr>
      <tr><td>年度予算・設備投資</td><td>各社と本部で協議</td></tr>
      <tr><td>借入・大型投資・役員人事</td><td>各社と本部で協議</td></tr>
      <tr><td>経理・労務・情報管理のルール</td><td>グループ共通</td></tr>
    </tbody></table></div>
  </div>
</section>"""

HISTORY=f"""<section class="hist">
  <div class="w g2">
    <div class="rv">{head('History','沿革','')}</div>
    <ul class="hl rv"><li><time>2026</time><p>株式会社エッジアセット設立（東京都港区）　設立月 {TBD}</p></li><li><time>2026.10</time><p>コーポレートサイトを公開</p></li></ul>
  </div>
</section>""".replace('<h2></h2>','')

PFAQ_Q=[('小規模な案件でも検討してもらえますか。','はい。年商や棟数で一律に線を引くことはしていません。ノンネーム情報の段階で、検討できるかどうかをお伝えします。'),
        ('ノンネームの段階で、どこまでの情報が必要ですか。','エリア（都道府県）、事業内容、売上と営業利益の概算、譲渡を考える理由がわかれば、初回のご回答ができます。'),
        ('意向表明までの期間はどのくらいですか。','秘密保持契約の締結と資料のご提供から、通常2〜3週間を目安にしています。'),
        ('買い手側の手数料について教えてください。',f'ご紹介者さまとの契約内容に応じてご相談させてください。{TBD}'),
        ('売り手の社長と直接話してもいいですか。','ご紹介者さまの了承がある場合に限り、同席のうえでお話を伺います。')]
PFAQ=f"""<section class="pfaq">
  <div class="w tf">
    <div>{head('FAQ','ご紹介者さまからのご質問','')}</div>
    <div>{''.join(f'<details><summary><span class="q">Q.</span><span>{nb(q,6)}</span><span class="pm"></span></summary><div class="a"><span>A.</span>{P(a)}</div></details>' for q,a in PFAQ_Q)}</div>
  </div>
</section>""".replace('<h2></h2>','')
INFO=f"""<section class="info">
  <div class="w g2">
    <div class="rv">{head('Information','ご共有いただきたい情報','初回の|ご回答に|必要な情報')}</div>
    <ul class="chk2 rv">{''.join(f'<li><b>{a}</b><span>{W(b)}</span></li>' for a,b in [('所在地','都道府県・|主な施工エリア'),('事業内容','注文・規格・|リフォームの比率'),('業績','直近3期の|売上高・営業利益の|概算'),('規模','年間引渡し棟数・|従業員数'),('譲渡の理由','後継者不在・|引退時期など'),('ご希望','価格・|社長の処遇・|時期の目安')])}</ul>
  </div>
</section>"""
PREP=f"""<section class="prep">
  <div class="w g2">
    <div class="rv">{head('Before meeting','面談について','初回の面談で|伺うこと')}</div>
    <div class="rv">
      <ul class="chk2">{''.join(f'<li><b>{a}</b><span>{W(b)}</span></li>' for a,b in [('会社のこと','創業からの歩み、|強み、|社員構成'),('ご自身のこと','引退の時期、|ご家族の意向、|これからの関わり方'),('気がかりなこと','社員・施主様・|協力業者さんへの影響')])}</ul>
      <p class="pnote">{W('決算書などの|資料は、|初回は|不要です。|話せる範囲で|構いません。')}</p>
    </div>
  </div>
</section>"""
SERVICE_INTRO=f"""<section class="svint">
  <div class="w g2">
    <div class="rv">{head('Our support','支援の考え方','家づくりは|各社に、|それ以外は|グループで')}</div>
    <div class="rv">{P('工務店の強みは、地域の施主様との信頼関係と、現場の技術です。一方で、集客・採用・経理・仕入といった仕事は、会社の規模が小さいほど一社あたりの負担が重くなります。')}{P('エッジアセットは、この「家づくり以外の仕事」をグループで引き受けます。社長と社員が本来の仕事に時間を使えるようにすることが、私たちの支援の目的です。')}</div>
  </div>
</section>"""
PFEATURES=''

# ===================== columns, legal pages =====================
def art_body(blocks):
    out=[]
    for kind,txt in blocks:
        if kind=='h2': out.append(f'<h2>{W(txt)}</h2>')
        elif kind=='h3': out.append(f'<h3>{W(txt)}</h3>')
        elif kind=='p': out.append(P(txt))
        elif kind=='ul': out.append('<ul>'+''.join(f'<li>{x}</li>' for x in txt)+'</ul>')
        elif kind=='box': out.append(f'<div class="abox">{P(txt)}</div>')
        elif kind=='tbl': out.append('<div class="tbl"><table class="atbl">'+''.join('<tr>'+''.join(f'<t{"h" if i==0 or r==0 else "d"}>{c}</t{"h" if i==0 or r==0 else "d"}>' for i,c in enumerate(row))+'</tr>' for r,row in enumerate(txt))+'</table></div>')
    return '\n'.join(out)

ARTICLES=[
 dict(slug='column-1.html',date='2026.10.23',cat='事業承継の基礎',pid='Q6sCJFHCubc',
  title='工務店の事業承継、3つの選択肢と選び方',
  lead='後継者が決まっていない工務店の社長が取りうる道は、大きく分けて「親族・社員への承継」「第三者への譲渡（M&A）」「廃業」の3つです。それぞれの特徴と、選ぶときの判断軸を整理します。',
  blocks=[
   ('p','帝国データバンクの調査（2025年）では、建設業の後継者不在率は57.3%と、業種別で最も高い水準です。後継者が決まらないまま社長が高齢になると、選べる道は年々少なくなります。まずは選択肢を知り、早めに比べておくことが大切です。'),
   ('h2','選択肢1：親族・社員への承継'),
   ('p','もっとも自然に思える方法ですが、工務店では二つの壁があります。一つは、子どもが別の仕事に就いているなど、継ぐ意思のある人がいないこと。もう一つは、社員に継がせる場合に、株式を買い取る資金と、借入の個人保証を引き受ける覚悟が求められることです。'),
   ('p','社員承継を選ぶなら、株価対策や、金融機関との保証の引き継ぎの交渉に、数年単位の準備期間が必要です。'),
   ('h2','選択肢2：第三者への譲渡（M&A）'),
   ('p','会社を外部の会社やファンドに引き継ぐ方法です。社員の雇用と会社を残しながら、社長は株式の対価を受け取り、個人保証からも外れることができます。'),
   ('p','ただし、相手によって「その後」が大きく変わります。同業の大手に統合されれば、社名や部門が整理されることもあります。数年での売却を前提とする投資ファンドであれば、引き継いだ後にさらに別の会社へ売られる可能性があります。'),
   ('h2','選択肢3：廃業'),
   ('p','後継者も譲渡先も見つからない場合の最終手段です。注意したいのは、廃業すると引渡し済みの家の保証や定期点検を引き受ける会社がいなくなることです。地域で長く家を建ててきた会社ほど、施主様への影響は大きくなります。'),
   ('h2','比べるときの判断軸'),
   ('tbl',[['判断軸','確認すること'],['社名・ブランド','引き継いだ後も残るか'],['社員の雇用','雇用と給与水準が守られるか'],['施主様のアフター','保証・定期点検を誰が担うか'],['社長の個人保証','解除されるか'],['数年後の姿','再び売却される前提ではないか']]),
   ('box','どの方法にも長所と短所があります。大切なのは、社長ご自身が「何を残したいか」を先に決めておくことです。社名か、社員か、施主様との関係か。その優先順位がはっきりしていれば、相手選びで迷いにくくなります。'),
  ]),
 dict(slug='column-2.html',date='2026.10.23',cat='施主様・アフター',pid='-MVSfkR4xz4',
  title='工務店を譲渡したら、施主様の保証と点検はどうなる？',
  lead='会社を引き継ぐ相談で、多くの社長が最初に口にするのが「これまで建てた家の点検は誰が行くのか」という心配です。譲渡の方法ごとに、保証とアフターがどう扱われるかを整理します。',
  blocks=[
   ('h2','株式譲渡なら、保証は会社に残る'),
   ('p','株式譲渡は、会社の持ち主（株主）が変わるだけで、会社そのものは変わりません。そのため、施主様との工事請負契約や、そこに含まれる保証の約束は、原則としてそのまま会社に残ります。'),
   ('p','住宅瑕疵担保履行法にもとづく保険や供託の手続きも会社単位で行われているため、株式譲渡によって施主様の保護が途切れることはありません。'),
   ('h2','気をつけたいのは「人」と「記録」'),
   ('p','制度上は保証が残っても、実際に点検に伺う担当者がいなくなれば、施主様の安心は失われます。引き継ぎで確認しておきたいのは次の点です。'),
   ('ul',['定期点検の予定表と、過去の点検・修繕の記録','施主様ごとの担当者と、連絡の窓口','協力業者さんとの関係（修繕を頼める体制が続くか）','過去のクレームや、対応中の案件の有無']),
   ('h2','施主様へのお知らせは、いつ、どう伝えるか'),
   ('p','施主様へのお知らせは、社員への説明が終わってから行うのが一般的です。「社名も担当者も変わらない」「保証と点検はこれまでどおり続く」ことを、文書と口頭の両方でお伝えすると安心していただけます。'),
   ('box','エッジアセットでは、引渡し済みの家の保証・定期点検の継続を、株式譲渡契約の条項に書き込んでいます。点検の記録はデータで管理し、担当者が変わっても引き継げる状態をつくります。'),
  ]),
 dict(slug='column-3.html',date='2026.10.23',cat='許認可・法務',pid='4UVtFIfK1eo',
  title='建設業許可は引き継げる？株式譲渡と事業譲渡の違い',
  lead='工務店の譲渡で必ず確認が必要なのが、建設業許可の扱いです。譲渡の方法によって、許可がそのまま使えるか、手続きが必要かが変わります。',
  blocks=[
   ('h2','株式譲渡：許可は会社に残る'),
   ('p','株式譲渡では、許可を持っている会社そのものが存続するため、建設業許可は原則としてそのまま使えます。ただし、許可の要件を満たし続ける必要があります。'),
   ('p','特に注意したいのが、経営業務の管理責任者（経管）と専任技術者です。譲渡にともなって社長が退任し、その社長が経管を兼ねていた場合は、後任を置かないと要件を満たせなくなります。誰がいつ交代するかを、譲渡の前に設計しておくことが欠かせません。'),
   ('h2','事業譲渡：事前の認可で承継できる'),
   ('p','2020年10月に施行された改正建設業法により、事業譲渡・合併・会社分割の場合でも、事前に許可行政庁の認可を受ければ、建設業許可を承継できるようになりました。改正前は、譲り受けた側が新たに許可を取り直す必要があり、その間は工事を受けられない空白期間が生じていました。'),
   ('h2','比べてみると'),
   ('tbl',[['','株式譲渡','事業譲渡'],['許可','会社に残る','事前の認可で承継'],['契約・保証','会社に残る','個別に引き継ぎが必要'],['主な注意点','経管・専任技術者の後任','認可申請のスケジュール']]),
   ('box','工務店の事業承継では、許可・施主様との契約・保証をまとめて引き継げる株式譲渡が選ばれることが多くあります。どの方法が適しているかは会社の状況によって変わるため、早めに専門家に相談してください。'),
  ]),
]
for a in ARTICLES:
    a['excerpt']=a['lead'][:60]+'…'

def col_card(a):
    return f'''<a class="cc rv" href="{a['slug']}"><div class="ph">{img(a['pid'],'',1200)}</div><div class="cc-tx"><p class="cc-m"><time>{a['date']}</time><span>{a['cat']}</span></p><h3>{W(a['title'])}</h3><p class="cc-e">{a['excerpt']}</p></div></a>'''
COLLIST=f"""<section class="collist"><div class="w"><div class="cg">{''.join(col_card(a) for a in ARTICLES)}</div></div></section>"""
TOPCOL=f"""<section class="topcol">
  <div class="w">
    {head('Column','コラム','工務店の|事業承継を|考える','事業承継の選択肢、施主様へのアフター、建設業許可。社長が判断に迷うポイントを解説しています。')}
    <div class="cg">{''.join(col_card(a) for a in ARTICLES)}</div>
    <a class="tl" href="column.html" style="margin-top:36px">コラム一覧へ {AR}</a>
  </div>
</section>"""
def article_page(a):
    others=''.join(col_card(o) for o in ARTICLES if o is not a)
    return f"""<section class="arthero"><div class="w aw"><p class="crumb"><a href="index.html">トップ</a><span>/</span><a href="column.html">コラム</a></p><p class="cc-m"><time>{a['date']}</time><span>{a['cat']}</span></p><h1>{W(a['title'])}</h1></div></section>
<div class="artimg"><div class="ph">{img(a['pid'],a['title'],1800,False)}</div></div>
<article class="art"><div class="w aw">
  <p class="alead">{a['lead']}</p>
  {art_body(a['blocks'])}
  <div class="acta"><p>{W('事業承継について、|まずは話を|聞いてみませんか。')}</p><a class="btn btn-navy" href="contact.html">無料で相談する {AR}</a></div>
  <p class="anote">本記事は一般的な情報の提供を目的としたもので、個別の案件についての法的・税務上の助言ではありません。</p>
</div></article>
<section class="artmore"><div class="w"><p class="sh-ja">ほかのコラム</p><div class="cg c2">{others}</div></div></section>"""

def legal(title,en,items,updated):
    body=''.join(f'<h2>{W(h)}</h2>'+''.join(P(x) if not isinstance(x,list) else '<ul>'+''.join(f'<li>{y}</li>' for y in x)+'</ul>' for x in xs) for h,xs in items)
    return phero(en,title,'','rD28m9BmXVs')+f'<article class="art legal"><div class="w aw">{body}<p class="anote">{updated}</p></div></article>'
PRIVACY=legal('プライバシーポリシー','Privacy policy',[
 ('基本方針',['株式会社エッジアセット（以下「当社」）は、お客様の個人情報を適切に取り扱うことが社会的責務であると考え、個人情報の保護に関する法律その他の関係法令を遵守し、以下のとおり個人情報を取り扱います。']),
 ('取得する個人情報',['当社は、お問い合わせフォーム、電話、面談等を通じて、氏名、会社名、メールアドレス、電話番号、ご相談内容その他お客様が提供する情報を取得します。']),
 ('利用目的',[['お問い合わせ・ご相談への回答および連絡のため','事業承継・株式取得等のご提案、検討および実行のため','面談日程の調整その他の連絡のため','当社サービスの改善のため']]),
 ('第三者への提供',['当社は、法令に定める場合を除き、ご本人の同意を得ることなく個人情報を第三者に提供しません。']),
 ('業務の委託',['当社は、利用目的の達成に必要な範囲で、個人情報の取扱いを外部に委託することがあります。この場合、委託先に対して必要かつ適切な監督を行います。']),
 ('安全管理措置',['当社は、個人情報の漏えい、滅失または毀損を防止するため、必要かつ適切な安全管理措置を講じます。']),
 ('アクセス解析について',['当社ウェブサイトでは、利用状況の把握のためにアクセス解析ツールを使用する場合があります。これらのツールはCookieを使用してデータを収集しますが、個人を特定する情報は含みません。Cookieはブラウザの設定により無効にできます。']),
 ('開示・訂正・利用停止等のご請求',['ご本人から個人情報の開示、訂正、追加、削除、利用停止等のご請求があった場合は、ご本人であることを確認のうえ、法令に従って速やかに対応します。']),
 ('お問い合わせ窓口',[f'株式会社エッジアセット　〒105-0022 東京都港区海岸2丁目5-1-1702　個人情報お問い合わせ窓口　メール：{TBD}']),
 ('改定',['当社は、法令の変更等に応じて本ポリシーを改定することがあります。改定後の内容は本ページに掲載した時点から効力を生じます。']),
],'制定日：2026年10月【確定後に記載】　株式会社エッジアセット　代表取締役　谷岡 佑亮')
TERMS=legal('サイトのご利用について','Terms of use',[
 ('著作権',['本サイトに掲載している文章・画像等の著作権は、当社または正当な権利者に帰属します。私的利用の範囲を超える無断での複製・転載を禁止します。']),
 ('免責事項',['本サイトの情報は、掲載時点での一般的な情報の提供を目的としています。内容の正確性には注意を払っていますが、その完全性・最新性を保証するものではありません。本サイトの利用によって生じた損害について、当社は責任を負いません。']),
 ('リンクについて',['本サイトへのリンクは原則として自由です。ただし、当社の信用を損なうおそれのあるサイトからのリンクはお断りします。']),
 ('写真について',['本サイトに掲載している写真の一部は、イメージ素材（Unsplash）を使用しています。']),
],'株式会社エッジアセット')
NOTFOUND=f"""<section class="nf"><div class="w"><p class="pen">404</p><h1>ページが見つかりませんでした</h1>{P('お探しのページは移動または削除された可能性があります。')}<a class="btn btn-navy" href="index.html">トップへ戻る {AR}</a></div></section>"""
