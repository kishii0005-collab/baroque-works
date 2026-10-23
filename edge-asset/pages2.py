# cases (list + detail), flow page, cost section, and sub-page accents. exec'd from build.py after more.py
NT=' target="_blank" rel="noopener"'

# ---------- sub-page hero: copy on navy, photo bleeding to the right edge ----------
def phero(en,ja,lead,pid,no=None):
    n=f'<p class="pno"><b>{no}</b>EDGE ASSET</p>' if no else ''
    return f"""<section class="phero">
  <div class="pg-ph"><div class="ph">{img(pid,'',2000,False)}</div><span class="pg-blk" aria-hidden="true"></span></div>
  <div class="w"><p class="crumb"><a href="index.html">トップ</a><span>/</span>{ja}</p>{n}<p class="pen">{en}</p><h1>{W(ja)}</h1>{P(lead,'plead') if lead else ''}</div>
  <p class="pscroll" aria-hidden="true">Scroll</p>
</section>"""

def band(pid,en,text,sub=''):
    return f"""<section class="band">
  <div class="ph">{img(pid,'',2000)}</div>
  <div class="w rv"><p class="band-en">{en}</p><p class="band-t">{W(text)}</p>{P(sub,'band-s') if sub else ''}</div>
</section>"""

def kpis(items,dark=False):
    li=''.join(f'<li class="rv"><b>{n}<small>{u}</small></b><span>{W(t)}</span></li>' for n,u,t in items)
    return f'<section class="kpi{" dark" if dark else ""}"><div class="w"><ul>{li}</ul></div></section>'

def nextlink(href,en,ja):
    return f"""<section class="nextp"><a href="{href}"{NT} class="w"><span class="nx-k">Next page</span><span class="nx-en">{en}</span><span class="nx-ja">{ja}</span><span class="nx-ar" aria-hidden="true"></span></a></section>"""

# ---------- cost ----------
LEVERS=[('共同購買','住設・建材・構造材をグループでまとめて発注'),
 ('単価の見える化','品目別・取引先別に購入単価を一覧に'),
 ('実行予算','着工前に現場ごとの予算を確定'),
 ('標準仕様','発注ミスと残材が出やすい品番を整理'),
 ('手戻り削減','図面チェックと工程表をグループで共通化'),
 ('間接費','保険・リース・車両・広告を共同契約')]
CSTEPS=[('Visualize','見える化','過去の発注を、品目別・取引先別に一覧にします。同じ商品を現場ごとに違う値段で買っていないか、相場より高い取引はどれかを確かめます。'),
 ('Negotiate','適正価格での交渉','相場や他の仕入れ先の価格と比べ、根拠を示して交渉します。住設・建材はグループでまとめて発注し、1社では届かない条件を引き出します。'),
 ('Systemize','仕組み化','着工前の実行予算、発注のルール、標準仕様を整えます。一度下げた原価が、元に戻らない仕組みにします。')]
PARTNER=['品質・納期・価格の3つで評価します','一方的な値下げではなく、相場と発注量を根拠に交渉します','条件が折り合わない場合は、取引先の見直しも行います']
def sim_rows():
    out=''
    for rev in (3,6,10):
        cells=''.join((f'<td>{rev*p/10:g}<small>億円</small></td>' if rev*p>=10 else f'<td>{rev*p*1000:,}<small>万円</small></td>') for p in (1,2,3))
        out+=f'<tr><th>年商 {rev}億円</th>{cells}</tr>'
    return out
def pbars(dark=False):
    row=lambda k,c,g,o:f'<div class="pb-r"><p class="pb-k">{k}</p><div class="pb-bar"><i class="c" style="flex:{c}"><b>原価 {c}</b></i><i class="g" style="flex:{g}"><b>販管費 {g}</b></i><i class="o" style="flex:{o}"><b>{o}</b></i></div></div>'
    return f"""<div class="pbars{' dk' if dark else ''} rv">
  {row('いま',75,20,5)}{row('原価率 −2pt',73,20,7)}
  <div class="pb-res"><p class="pb-big">営業利益 <b>1.4</b>倍</p><p class="pb-cap">{W('売上が|同じでも、|原価率が|2ポイント|下がるだけで|営業利益は|5から7へ。')}</p></div>
  <p class="pb-note">売上を100としたモデル（原価率75%・販管費率20%の場合）。濃い青が営業利益です。</p>
</div>"""
COST=f"""<section class="cost" id="cost">
  <div class="w">
    {head('Cost','原価の改善','原価の|1ポイントが、|会社の|利益を|変える。','工務店の利益を一番大きく左右するのは原価です。発注量をまとめた交渉と数字の管理で、仕入れ値を適正な水準に見直し、営業利益率の最大化に取り組みます。')}
    <div class="cs-why">
      <div class="cs-wt rv"><p class="cs-k">Why cost</p><h3>{W('原価2ポイントの|改善は、|売上を|8%|伸ばすのと|同じ効果。')}</h3>{P('年間25棟の会社なら、2棟多く受注するのと同じ利益です。受注を増やすには広告費も人も時間もかかりますが、原価の見直しは、いま受けている仕事のままで取り組めます。')}</div>
      {pbars()}
    </div>
    <ol class="cs-steps">{''.join(f'<li class="rv"><p class="cs-sn">STEP {i+1:02d}<span>{e}</span></p><h3>{W(h)}</h3>{P(t)}</li>' for i,(e,h,t) in enumerate(CSTEPS))}</ol>
    <div class="cs-lv rv"><p class="cs-k">6つの打ち手</p><ul>{''.join(f'<li><b>{h}</b><span>{W(t)}</span></li>' for h,t in LEVERS)}</ul></div>
    <div class="cost-b">
      <div class="sim rv">
        <p class="sim-k">原価率が下がると、粗利はどれだけ増えるか</p>
        <div class="tw"><table><thead><tr><th></th><th>1ポイント</th><th>2ポイント</th><th>3ポイント</th></tr></thead><tbody>{sim_rows()}</tbody></table></div>
        <p class="sim-n">{W('年間の|粗利の|増加額（単純計算）。|年商6億円の|会社で|原価率が|2ポイント|下がれば、|粗利は|年1,200万円|増えます。')}</p>
      </div>
      <div class="notdo rv">
        <p class="nd-k">取引先との向き合い方</p>
        <ul>{''.join(f'<li>{W(x)}</li>' for x in PARTNER)}</ul>
        {P('いい仕事をしてくださる協力業者さんとは長くお付き合いし、グループの他社の現場もお願いしていきます。')}
      </div>
    </div>
  </div>
</section>"""
TOPCOST=f"""<section class="tcost dark">
  <div class="w">
    <div class="tc-l rv">
      <p class="sh-en" aria-hidden="true">Cost</p><p class="sh-ja">原価の改善</p>
      <h2>{W('利益は、|売上より先に|原価で|決まる。')}</h2>
      {P('仕入れ値を相場と照らして見直し、住設・建材はグループでまとめて発注。着工前に実行予算を組む。発注量をまとめた交渉と数字の管理で、営業利益率の最大化に取り組みます。')}
      <a class="btn btn-white" href="service.html#cost"{NT}>原価改善の進め方を見る {AR}</a>
    </div>
    {pbars(True)}
  </div>
</section>"""

# ---------- cases ----------
CASES=[
 dict(slug='case-1',tag='後継者不在',en='Succession',pid='TJ4CndIc9z8',alt='地方都市の住宅街',
  title='子どもは|別の道へ。|社員に|継がせるには|資金が|足りない。',
  short='株式はグループが引き受け、経営は番頭格の社員が継ぐ。所有と経営を分けて、社内承継を実現した想定例です。',
  prof=[('エリア','地方都市'),('事業','注文住宅・リフォーム'),('規模','年商 約8億円／年間引き渡し 25棟'),('社員','18名'),('社長','68歳・創業者')],
  before=['長男は県外で会社員。家業を継ぐ意思はない','番頭格の工事部長（52歳）に継がせたいが、株式を買い取る資金を用意できない','社長個人が、会社の借入 約3億円の連帯保証を負っている','引き渡したOB施主様 約600棟の定期点検が、今後も続く'],
  trigger='取引銀行との面談で事業承継が話題に上ったことをきっかけに、仲介会社経由でご相談いただきました。ご希望は「会社を残すこと」と「部長を社長にすること」の両立でした。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','2年間、代表権のない会長として残留'),('次の社長','工事部長が1年目に取締役、3年目に代表取締役へ'),('社名・屋号','変更なし'),('雇用・給与','全員継続。給与水準は維持'),('個人保証','クロージング時に金融機関と協議し、解除'),('期間','初回面談からクロージングまで 約7ヶ月')],
  steps=[('初日','社長と私たちで、全社員に直接ご説明'),('30日後','月次決算をグループ本部で締める体制へ移行'),('100日後','部長を交えた経営会議を毎月開催。実行予算の管理を開始'),('1年後','部長が取締役に就任。現場監督を2名採用')],
  change=[('月次の数字','年1回の決算のみ','翌月10日に確定'),('社長の個人保証','約3億円','解除'),('次の社長','未定','社内の工事部長に決定')],
  voice='一番怖かったのは、社員に「売られた」と思われることでした。説明の場に一緒に立ってもらえたのが大きかった。',
  point='社内承継の一番の壁は、株式を買い取る資金です。グループが株式を引き受け、経営は社員が継ぐ形にすれば、資金の問題と「誰が継ぐか」の問題を切り分けられます。'),
 dict(slug='case-2',tag='成長の壁',en='Growth',pid='4UVtFIfK1eo',alt='木造の骨組み',
  title='受注は|あるのに、|人が|採れず|年20棟から|伸びない。',
  short='社長は続投し、株式の一部も持ち続ける。採用・集客・管理部門をグループで支え、社長が営業と現場に戻った想定例です。',
  prof=[('エリア','首都圏郊外'),('事業','注文住宅'),('規模','年商 約6億円／年間引き渡し 20棟'),('社員','14名'),('社長','55歳・二代目')],
  before=['受注残はあるが、現場監督が2名で年20棟が上限','求人を出しても、応募は年に数件','社長が営業・設計確認・経理まで一人で兼任','Web集客は外注任せで、成果が数字で見えていない'],
  trigger='「会社を売りたい」ではなく、「伸ばすための仲間がほしい」というご相談でした。社長の続投を前提に検討を進めました。',
  scheme=[('取得する株式','70%（社長が30%を継続保有）'),('社長の処遇','代表取締役として続投'),('社名・屋号','変更なし'),('雇用・給与','全員継続'),('個人保証','借り換えにあわせて段階的に解除'),('期間','初回面談からクロージングまで 約5ヶ月')],
  steps=[('初日','社長と私たちで、全社員に直接ご説明'),('30日後','問い合わせ数・来場数・成約率を、グループ共通の管理表に統一'),('100日後','グループ合同採用で、現場監督と設計の募集を開始'),('1年後','現場監督4名体制へ。経理・総務はグループ本部が担当')],
  change=[('現場監督','2名','4名'),('年間引き渡し','20棟','28棟（目標）'),('社長の事務作業','週 約15時間','週 約2時間')],
  voice='社長を続けられるなら、という条件で話を聞きました。営業と現場に戻れたのが何よりです。',
  point='成長期の会社に足りないのは、資金より「人と仕組み」です。株式の一部を持ち続けてもらうことで、社長と私たちが同じ方向を向いて会社を伸ばせます。'),
 dict(slug='case-3',tag='廃業の検討',en='Continuity',pid='q1tyQip5AQQ',alt='大きな窓のある室内',
  title='体力的に|限界。|でも|施主様の|アフターだけは|残したい。',
  short='社名とアフター窓口を残し、近隣のグループ会社と管理部門・仕入れを共通化。社長は半年で引退した想定例です。',
  prof=[('エリア','地方の郡部'),('事業','リフォーム中心'),('規模','年商 約3億円'),('社員','6名'),('社長','72歳・創業者')],
  before=['体力的に限界で、後継者はいない','廃業すると、OB施主様 約1,200件のアフターの行き先がなくなる','建設業許可の常勤役員等（いわゆる経管）の要件を満たすのが、社長しかいない','債務超過ではないが、利益はほぼゼロ'],
  trigger='廃業の手続きを相談していた顧問税理士からのご紹介です。「OB施主さんのアフターだけは残したい」というお話から始まりました。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','半年で引退。その後は非常勤の相談役'),('社名・アフター窓口','変更なし'),('建設業許可','要件を満たす人材をグループから役員として迎え、許可を維持'),('管理部門','近隣のグループ会社と経理・発注を共通化'),('期間','初回面談からクロージングまで 約5ヶ月')],
  steps=[('初日','社長と私たちで、全社員に直接ご説明'),('30日後','OB施主様へ、点検の窓口と担当者が変わらないことをご案内'),('100日後','近隣のグループ会社と、発注・経理を共通化'),('1年後','現場責任者を中心とした体制が定着。相談役の社長は月1回の会議に参加')],
  change=[('営業利益','ほぼゼロ','黒字化（目標）'),('OB施主様の窓口','廃業で失われる可能性','継続'),('資材の発注','社長個人の付き合いで分散','グループの共同購買')],
  voice='やめる以外に道はないと思っていました。電話番号も担当者もそのままで、お客さんに迷惑をかけずに済みました。',
  point='規模が小さく利益が薄くても、OB施主様というストックと地域の信用には価値があります。管理部門と仕入れを近くのグループ会社と分け合えば、1社では難しかった採算が合うようになります。'),
 dict(slug='case-4',tag='粗利の低下',en='Cost',pid='pcYN7Pi8_BQ',alt='夕暮れの住宅街',
  title='資材は|上がり、|粗利は|3年で|5ポイント|下がった。',
  short='グループ入り後に仕入れ値の見直し、発注の集約、実行予算の徹底で粗利を立て直し、2年後に社内の後継者へ社長を引き継ぐ想定例です。',
  prof=[('エリア','中核市'),('事業','注文住宅・分譲'),('規模','年商 約10億円／年間引き渡し 35棟'),('社員','24名'),('社長','62歳・二代目')],
  before=['資材価格の上昇を販売価格に転嫁しきれず、粗利率が3年で約5ポイント低下','発注は担当者ごとにばらばら。同じ住設を、現場ごとに違う価格で購入','実行予算を組まずに着工し、赤字の現場が引き渡し後に判明','後継者候補はいるが、業績の悪化で承継に踏み切れない'],
  trigger='「数字が見えないまま、次の社長に会社を渡すわけにはいかない」。承継の前に、立て直しも一緒に進めたいというご相談でした。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','2年間続投し、その後は社内の後継者へ'),('社名・屋号','変更なし'),('雇用・給与','全員継続'),('取引先','品質・納期・価格を基準に、仕入れ値と外注費を見直し'),('期間','初回面談からクロージングまで 約6ヶ月')],
  steps=[('初日','社長と私たちで、全社員に直接ご説明'),('30日後','過去2年の全現場の原価を洗い出し、品目別の購入単価を一覧化'),('100日後','住設・建材をグループの共同購買に切り替え、主要な取引先と単価を交渉。実行予算を必須に'),('1年後','標準仕様を整理し、図面チェックの様式を統一して手戻りを削減')],
  change=[('実行予算','一部の現場のみ','全現場で着工前に作成'),('住設・建材の購入先','担当者ごとに分散','グループの共同購買に集約'),('粗利率','3年で約5ポイント低下','2ポイント改善が目標（粗利 年約2,000万円）')],
  voice='どこにいくら払っているのか、初めて全部が見えました。根拠のある交渉だったので、取引先とも揉めずに済みました。',
  point='原価は、まず「どこにいくら払っているか」を見える化し、相場と発注量を根拠に交渉することで下がります。着工前に数字を決める仕組みまで作れば、下がった原価は元に戻りません。立て直してから社長を交代すれば、次の社長の負担も軽くなります。'),
]
CASE_NOTE='掲載している事例は、よくあるご相談をもとにしたモデルケース（想定事例）です。実在の企業・数値ではありません。'

def case_card(c,i):
    pr=''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in c['prof'] if k in ('エリア','規模','社長'))
    return f"""<a class="ccase rv" href="{c['slug']}.html"{NT}>
  <div class="ph">{img(c['pid'],c['alt'],1200)}<span class="cc-no">CASE<b>{i+1:02d}</b></span></div>
  <div class="cc-tx"><p class="cc-tag"><span>{c['tag']}</span>{c['en']}</p><h3>{W(c['title'])}</h3>{P(c['short'])}<dl>{pr}</dl><span class="cc-more">詳しく見る {AR}</span></div>
</a>"""

CASELIST=f"""<section class="clist">
  <div class="w">
    {head('Model cases','モデルケース','4つの|ご相談の|かたち','後継者がいない、成長が止まった、廃業を考えている、粗利が下がり続けている。よくいただくご相談を、引き継ぎの形と、その後の1年まで含めてご紹介します。')}
    <div class="cgrid">{''.join(case_card(c,i) for i,c in enumerate(CASES))}</div>
    <p class="cnote">{CASE_NOTE}</p>
  </div>
</section>"""

TOPCASES=f"""<section class="tcases" id="cases">
  <div class="w">
    {head('Case','モデルケース','こんな|ご相談を|お受け|しています','よくあるご相談を、条件を変えた想定事例としてまとめました。カードを押すと、引き継ぎの形とその後の1年を別タブでご覧いただけます。')}
    <div class="cgrid">{''.join(case_card(c,i) for i,c in enumerate(CASES))}</div>
    <div class="tc-foot"><p class="cnote">{CASE_NOTE}</p><a class="btn btn-navy" href="cases.html"{NT}>事例一覧を見る {AR}</a></div>
  </div>
</section>"""

def case_page(c,i):
    nxt=CASES[(i+1)%len(CASES)]
    others=''.join(case_card(o,j) for j,o in enumerate(CASES) if o is not c)
    prof=''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in c['prof'])
    return f"""<section class="chero">
  <div class="ph">{img(c['pid'],c['alt'],2000,False)}</div>
  <div class="w">
    <p class="crumb"><a href="index.html">トップ</a><span>/</span><a href="cases.html">モデルケース</a><span>/</span>CASE {i+1:02d}</p>
    <p class="ch-no">CASE <b>{i+1:02d}</b><span>{c['tag']}</span></p>
    <h1>{W(c['title'])}</h1>
    {P(c['short'],'plead')}
  </div>
</section>
<section class="cprof"><div class="w"><dl>{prof}</dl></div></section>
<section class="cbody">
  <div class="w cb-grid">
    <aside class="cb-side"><p class="cb-k">Contents</p><ol><li><a href="#c-before">ご相談前の状況</a></li><li><a href="#c-scheme">引き継ぎの形</a></li><li><a href="#c-after">グループ入り後の1年</a></li><li><a href="#c-change">変わったこと</a></li><li><a href="#c-point">この事例のポイント</a></li></ol><a class="btn btn-navy" href="contact.html"{NT}>似た状況を相談する {AR}</a></aside>
    <div class="cb-main">
      <div class="cb-sec rv" id="c-before"><p class="cb-n">01</p><h2>ご相談前の状況</h2><ul class="cb-iss">{''.join(f'<li>{x}</li>' for x in c['before'])}</ul><p class="cb-trg"><b>ご相談のきっかけ</b>{nb(c['trigger'])}</p></div>
      <div class="cb-sec rv" id="c-scheme"><p class="cb-n">02</p><h2>引き継ぎの形</h2><table class="cb-tbl">{''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k,v in c['scheme'])}</table></div>
      <div class="cb-sec rv" id="c-after"><p class="cb-n">03</p><h2>グループ入り後の1年</h2><ol class="cb-tl">{''.join(f'<li><span>{t}</span><p>{x}</p></li>' for t,x in c['steps'])}</ol></div>
      <div class="cb-sec rv" id="c-change"><p class="cb-n">04</p><h2>変わったこと</h2><div class="cb-ch">{''.join(f'<div class="cb-c"><p class="cb-ck">{k}</p><p class="cb-b"><small>Before</small>{b}</p><p class="cb-a"><small>After</small>{a}</p></div>' for k,b,a in c['change'])}</div></div>
      <blockquote class="cb-voice rv"><p>{nb(c['voice'])}</p><cite>社長の声（想定）</cite></blockquote>
      <div class="cb-sec rv" id="c-point"><p class="cb-n">05</p><h2>この事例のポイント</h2>{P(c['point'],'cb-pt')}</div>
      <p class="cnote">{CASE_NOTE}</p>
    </div>
  </div>
</section>
<section class="cother"><div class="w">{head('Other cases','ほかのモデルケース','ほかの|ご相談の|かたち')}<div class="cgrid c3">{others}</div></div></section>
""" + nextlink(f"{nxt['slug']}.html",f"Case {(i+1)%len(CASES)+1:02d}",nxt['title'].replace('|',''))

# ---------- flow ----------
FSTEPS=[('初回面談','First meeting','1〜2時間','会社のこと、ご家族のこと、社長ご自身のこれからを伺います。私たちの考え方と、進め方もご説明します。この段階で何かを決める必要はありません。',['特になし（決算書がなくても構いません）'],'社長お一人'),
 ('秘密保持契約・資料のご提供','NDA & documents','2〜4週間','秘密保持契約を結んだうえで、会社の数字と体制を拝見します。社員名簿は匿名でも構いません。',['決算書 3期分','受注残・施工中物件の一覧','借入の一覧','社員構成（匿名可）'],'社長・顧問税理士'),
 ('条件のご提示','Letter of intent','2〜3週間','譲渡価格の考え方、取得する株式の割合、社長の処遇、雇用、引き継ぎ期間を書面でお示しします。納得いくまで何度でも話し合います。',['ご希望の条件（引退の時期、社員の処遇など）'],'社長・ご家族・顧問税理士'),
 ('詳細調査','Due diligence','1〜2ヶ月','財務・税務・法務・労務に加え、施工中の物件、保証と点検の履歴、建設業許可の要件まで、住宅会社ならではの論点を確認します。',['契約書・許可関係の書類','保証書・点検記録'],'社長・経理担当（必要に応じて）'),
 ('最終契約・お支払い','Closing','約1ヶ月','株式譲渡契約を結び、代金をお支払いします。社長の個人保証の解除について、金融機関と協議します。',['印鑑・株券など、手続きに必要な書類'],'社長・ご家族・金融機関'),
 ('ご説明と引き継ぎ','Post merger','6ヶ月〜','社員の皆さま、協力業者さん、施主様へのご説明に私たちも同席します。その後は100日の計画に沿って、無理のない順番で引き継ぎます。',['特になし'],'全員に公表')]
GANTT=[(0,1),(0.5,1.5),(1.5,2.3),(2.3,4),(4,5),(5,7.5)]
def gantt():
    rows=''.join(f'<li><span class="gn">{i+1:02d} {s[0]}</span><span class="gb"><i style="left:{a/7.5*100:.1f}%;width:{(b-a)/7.5*100:.1f}%"></i></span></li>' for i,(s,(a,b)) in enumerate(zip(FSTEPS,GANTT)))
    months=''.join(f'<span>{m}</span>' for m in ['0','1','2','3','4','5','6','7ヶ月'])
    return f'<div class="gantt rv"><p class="g-k">標準的なスケジュール</p><ol>{rows}</ol><p class="gm">{months}</p></div>'
FLOWDETAIL=f"""<section class="fdet">
  <div class="w">
    {head('Process','ご相談から引き継ぎまで','6つの|ステップで、|最終契約まで|通常は|半年前後です','急いで決めていただく必要はありません。各段階で、何をして、何をご用意いただき、誰にまで話が伝わるのかを先にお伝えします。')}
    {gantt()}
    <ol class="fsteps">{''.join(f'''<li class="rv"><div class="fs-h"><span class="fs-n">STEP {i+1:02d}</span><p class="fs-en">{e}</p><h3>{W(h)}</h3><p class="fs-t">期間の目安　{t}</p></div><div class="fs-b">{P(d)}<div class="fs-m"><div><p class="fs-k">ご用意いただくもの</p><ul>{''.join(f'<li>{x}</li>' for x in prep)}</ul></div><div><p class="fs-k">話が伝わる範囲</p><p class="fs-who">{who}</p></div></div></div></li>''' for i,(h,e,t,d,prep,who) in enumerate(FSTEPS))}</ol>
  </div>
</section>"""
SECRET=f"""<section class="secret dark">
  <div class="w">
    {head('Confidential','秘密を守るために','最終契約までは、|ご了承なく|社員や取引先に|お伝えしません')}
    <ul class="sc-l">{''.join(f'<li class="rv"><span>{n}</span><h3>{W(h)}</h3>{P(t)}</li>' for n,h,t in [('01','面談は社外か|オンラインで','ご相談の段階で会社に伺うことはありません。ご自宅の近く、私たちの事務所、またはオンラインで行います。'),('02','連絡方法は|事前に決める','郵送物や電話は、社長と決めた方法でのみご連絡します。会社の代表番号にお電話することはありません。'),('03','秘密保持契約は|初回から','ご希望があれば、初回の面談の前に秘密保持契約を結びます。')])}</ul>
  </div>
</section>"""
THINK=f"""<section class="think">
  <div class="w grid">
    <div class="rv">{head('Before you talk','ご相談の前に','考えておくと|話が|早いこと','決まっていなくても構いません。面談の中で一緒に整理します。')}</div>
    <ol class="tk-l rv">{''.join(f'<li><span>Q{i+1}</span>{W(x)}</li>' for i,x in enumerate(['いつ頃までに、|社長を|退きたいか','引き継ぎ後も、|会社に|関わりたいか','社員の|誰に、|どんな役割を|任せたいか','ご家族は|株式や|会社のことを|どう考えているか','会社の|借入と、|ご自身の|個人保証の|状況']))}</ol>
  </div>
</section>"""
FLOWPAGE=FLOWDETAIL+SECRET+THINK

# ---------- page bodies ----------
SVC_KPI=kpis([('4','領域','グループで|支える|仕事'),('100','日','引き継ぎの|計画'),('30','年','保有を|前提に|経営'),('0','円','ご相談の|費用')])
COMPANY_BAND=band('-MVSfkR4xz4','Our stance','社名も、|社員も、|施主様との|約束も。','引き継ぐのは、株式だけではありません。')
SERVICE_BAND=band('pcYN7Pi8_BQ','Cost','適正な|仕入れ値が、|利益を|残す。','適正な仕入れ値で、利益が残る構造をつくります。')
CASES_BAND=band('Q6sCJFHCubc','Your case','同じ会社は、|ひとつも|ありません。','事例と違う状況でも、まずはお話を伺います。')
FLOW_BAND=band('a8A-z_ZPEC0','No rush','決めるのは、|社長です。','どの段階でも、立ち止まったり、お断りいただいたりして構いません。')

# ---------- representative profile (company page) ----------
PROFILE=f"""<section class="prof" id="profile">
  <div class="w">
    {head('Profile','代表プロフィール','理論と実務を、|現場で|つなぐ。')}
    <div class="pf-g">
      <div class="pf-card rv"><p class="pf-role">代表取締役</p><p class="pf-name">谷岡 佑亮</p><p class="pf-en">Yusuke Tanioka</p>
        <ul class="pf-tags">{''.join(f'<li>{t}</li>' for t in ['経営再建','成長戦略','人材採用','営業体制の構築','業務改善','建築業界'])}</ul></div>
      <div class="pf-tx rv">
        {P('株式会社船井総合研究所で、コンサルタントとして上位0.5%の年間粗利獲得実績を複数年にわたって納めました。経営再建や成長戦略の実行支援を中心に、現場に寄り添った実務型のコンサルティングに取り組んできました。')}
        {P('同社を退職後も複数の事業の運営に携わりながら、建築業界をはじめとする企業の人材採用、営業体制の構築、業務改善などを支援しています。')}
        {P('理論と実務をつなぐ進め方を大切にしています。現在は株式会社エッジアセットの代表として、地域の工務店・住宅会社の事業承継とグループ経営に取り組んでいます。')}
        <ol class="pf-tl">{''.join(f'<li><span>{e}</span><b>{h}</b>{P(t)}</li>' for e,h,t in [('Consulting','船井総合研究所','経営再建・成長戦略の実行支援。上位0.5%の年間粗利獲得実績を複数年にわたり達成。'),('Operation','事業運営と支援','複数の事業を運営しながら、建築業界を中心に採用・営業・業務改善を支援。'),('Edge Asset','代表取締役','工務店・住宅会社の事業承継とグループ経営に取り組む。')])}</ol>
      </div>
    </div>
  </div>
</section>"""

# ---------- top page: plain-language explainer (also carries search keywords) ----------
TOPSEO=f"""<section class="tseo">
  <div class="w">
    {head('About succession','工務店の事業承継とM&A','工務店・|住宅会社の|M&A・|事業承継を|お考えの方へ','後継者が決まっていない、受注が減って先が見えない、社員と施主様の今後が心配。そんな社長のために、事業承継の基本と、エッジアセットの考え方をまとめました。')}
    <div class="ts-g">
      <article class="rv"><p class="ts-n">01</p><h3>{W('建設業は、|後継者が|いない割合が|最も高い業種です')}</h3>{P('その割合は57.3%（帝国データバンク、2025年）。子どもが別の道に進んだ、社員に継がせるには株式を買い取る資金が足りない。黒字であっても、継ぐ人がいないために廃業を選ぶ工務店・住宅会社は少なくありません。廃業すれば、引き渡し済みの家の保証や定期点検を担う会社もなくなります。')}</article>
      <article class="rv"><p class="ts-n">02</p><h3>{W('株式譲渡なら、|会社も許可も|保証も残ります')}</h3>{P('第三者への事業承継（M&A）で多く選ばれるのが株式譲渡です。会社の持ち主が変わるだけなので、社名、社員の雇用、建設業許可、施主様との契約と保証は、原則としてそのまま会社に残ります。社長は株式の対価を受け取り、借入の個人保証からも外れることができます。')}</article>
      <article class="rv"><p class="ts-n">03</p><h3>{W('エッジアセットは、|住宅会社専門の|長期保有グループです')}</h3>{P('私たちは、引き継いだ会社を数年で売却することを前提にしていません。社名と現場は各社に残し、集客・採用・財務・仕入れなど、規模が小さいほど負担が重くなる仕事をグループ本部で支えます。原価と数字の管理で利益が残る経営をつくり、次の三十年へつなぎます。')}</article>
    </div>
    <div class="ts-links"><a class="tl" href="column-1.html">事業承継の3つの選択肢 {AR}</a><a class="tl" href="column-4.html">譲渡価格の考え方 {AR}</a><a class="tl" href="column-3.html">建設業許可の引き継ぎ {AR}</a></div>
  </div>
</section>"""

# ---------- service page FAQ ----------
SVCFAQ_Q=[('グループに入ると、家づくりの方針は変わりますか。','変わりません。設計・仕様・施主様との打ち合わせは、これまでどおり各社の判断です。グループが担うのは、集客・採用・財務・仕入れなど、規模が小さいほど負担が重くなる仕事です。'),
 ('集客の支援では、具体的に何をしてもらえますか。','反響数・来場数・成約率をグループ共通の管理表で毎月集計し、Google広告・Meta広告の運用、ホームページのSEO対策、Googleマップ（MEO）の整備を本部が担います。見学会の企画や施主様との関係づくりは各社に残します。'),
 ('仕入れ先との取引はどうなりますか。','品質・納期・価格の3つを基準に見直します。相場や発注量を根拠に交渉し、条件が合う取引先とは長くお付き合いします。住設・建材はグループの共同購買に切り替えることで、1社では届かない条件を引き出します。'),
 ('月次決算は、社内の誰が担当しますか。','グループ本部が締めます。各社には日々の伝票や請求書の整理をお願いし、翌月10日までに数字を共有します。経理担当の方の負担は、多くの場合いまより軽くなります。'),
 ('採用した社員は、どの会社に所属しますか。','各社の社員として採用し、配属します。グループ合同で説明会や求人を行うことで、一社では出せない規模で応募を集めます。グループ内の応援や異動は、ご本人の希望を踏まえて行います。')]
SVCFAQ=f"""<section class="topfaq">
  <div class="w tf">
    <div>{head('FAQ','支援についてのご質問','')}<a class="tl" href="contact.html#faq">すべての質問を見る {AR}</a></div>
    <div>{''.join(f'<details><summary><span class="q">Q.</span><span>{nb(q,6)}</span><span class="pm"></span></summary><div class="a"><span>A.</span>{P(a)}</div></details>' for q,a in SVCFAQ_Q)}</div>
  </div>
</section>""".replace('<h2></h2>','')

# ---------- structure helpers (trust bar, in-page index, closing CTA, contact aside, slim team) ----------
TRUST=f"""<section class="trust" aria-label="エッジアセットの特徴">
  <div class="w"><ul>{''.join(f'<li><span class="tr-k">{k}</span><b>{W(b)}</b><small>{s}</small></li>' for k,b,s in [
    ('Focus','工務店・|住宅会社専門','住宅業界の事業承継だけを扱います'),
    ('Ownership','売らない|長期保有','数年での売却を前提にしません'),
    ('Leadership','船井総研出身の|代表','在籍時、上位0.5%の粗利獲得実績'),
    ('Confidential','初回から|秘密保持','社外・オンラインで面談します')])}</ul></div>
</section>"""

def subnav(items):
    return f'<nav class="subnav" aria-label="このページの内容"><div class="w"><span class="sn-k">Index</span><ul>{"".join(f"<li><a href=\"#{i}\">{t}</a></li>" for i,t in items)}</ul></div></nav>'

def close(h='まずは、|話を|聞いてみる|だけで|構いません。',p='ご相談は無料です。社名を伏せたままでも、決算書がなくても構いません。'):
    return f"""<section class="closing">
  <div class="w">
    <div class="cl-t"><p class="cl-en">Contact</p><h2>{W(h)}</h2>{P(p)}</div>
    <div class="cl-a">
      <a class="cl-b" href="contact.html"{NT}><span>フォームで相談する</span><small>2営業日以内にご連絡します</small><i class="ar"></i></a>
      <a class="cl-b tel" href="tel:0300000000"><span>03-0000-0000</span><small>平日 9:00–18:00</small><i class="ar"></i></a>
    </div>
  </div>
</section>"""
CLOSE=close()
CLOSE_SVC=close('支援の中身を、|御社の|数字で|ご説明します。','どの支援から始めるかは、会社ごとに違います。現状を伺ったうえで、最初の100日の進め方をご提案します。')
CLOSE_CO=close('代表が、|直接|お話を|伺います。','面談には代表の谷岡が伺います。社外の会議室でも、オンラインでも構いません。')
CLOSE_CASE=close('似た状況でしたら、|そのまま|ご相談ください。','事例と条件が違っていても構いません。会社の状況を伺い、取りうる形をご説明します。')
CLOSE_FLOW=close('まずは、|初回面談の|日程だけ|決めませんか。','初回面談で何かを決めていただく必要はありません。1〜2時間、お話を伺うところから始めます。')

CONTACT_ASIDE=f"""<aside class="side ca">
  <p class="ca-k">After sending</p>
  <h3>送信後の流れ</h3>
  <ol>{''.join(f'<li><b>{n}</b><span>{W(t)}</span></li>' for n,t in [('01','2営業日以内に、|代表から|ご連絡します'),('02','日時と場所を|決めます（社外・|オンライン）'),('03','初回面談。|決算書が|なくても|構いません')])}</ol>
  <p class="ca-sec">{nb('秘密保持契約は、ご希望があれば初回面談の前に結べます。会社の代表番号にお電話することはありません。')}</p>
  <p class="ca-tel"><span>お電話でのご相談</span>03-0000-0000<small>平日 9:00–18:00　夜間・土日も調整します</small></p>
</aside>"""

TEAM2=f"""<section class="team" id="team">
  <div class="w">
    {head('Team','体制','住宅業界の|実務を|知るチームで、|引き継ぎます','会社を託す相手は、ファンドの名前ではなく人です。代表に加え、経営支援と専門家のチームでグループ入りを支えます。')}
    <div class="tm2">{''.join(f'<article class="rv"><p class="t2-r">{r}</p><h3>{n}</h3>{P(t)}{lk}</article>' for r,n,t,lk in [
      ('代表取締役','谷岡 佑亮','全体の統括と、各社の社長との経営会議を担当します。',f'<a class="tl" href="#profile">プロフィールを見る {AR}</a>'),
      ('取締役／グループ経営支援',TBD,'集客・採用・財務の実務を担当します。',''),
      ('顧問（税理士）',TBD,'事業承継税制・株価算定を担当します。',''),
      ('顧問（弁護士）',TBD,'株式譲渡契約・許認可を担当します。','')])}</div>
  </div>
</section>"""
