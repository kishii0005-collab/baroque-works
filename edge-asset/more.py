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
