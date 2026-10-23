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
LEVERS=[('01','共同購買','住設機器・建材・構造材を、グループでまとめて発注します。メーカーや商社と年間契約を結び、1社では届かない条件を引き出します。'),
 ('02','購入単価の見える化','同じ商品を、現場や担当者ごとに違う値段で買っていないか。過去の発注を品目別に一覧にして、まず「ばらつき」をなくします。'),
 ('03','実行予算の徹底','着工前に現場ごとの実行予算を組み、月次で予算と実績を比べます。赤字の現場を、引き渡し後ではなく工事中に見つけます。'),
 ('04','標準仕様の整理','選べる仕様の幅は残したまま、発注ミスや残材が出やすい品番を整理します。設計の自由度を下げることはしません。'),
 ('05','手戻りの削減','図面チェックと工程表の様式をグループで共通化し、やり直し工事や現場の待ち時間を減らします。'),
 ('06','間接費の共同契約','保険、リース、車両、基幹システム、広告媒体などをグループで契約し、固定費そのものを下げます。')]
NOT_DO=['協力業者さんの単価を一方的に下げること','支払サイトを延ばすこと','見えない部分の仕様や品質を落とすこと']
def sim_rows():
    out=''
    for rev in (3,6,10):
        cells=''.join(f'<td>{rev*p*1000:,}<small>万円</small></td>' for p in (1,2,3))
        out+=f'<tr><th>年商 {rev}億円</th>{cells}</tr>'
    return out
COST=f"""<section class="cost" id="cost">
  <div class="w">
    {head('Cost','原価の改善','原価は、|職人さんを|叩かずに|下げる。','工務店の利益を一番大きく左右するのは原価です。ただし、協力業者さんの手間賃を削って出した利益は長続きしません。グループの規模を使って「買い方」と「段取り」を変え、ムダな支出を減らします。')}
    <ol class="lever">{''.join(f'<li class="rv"><span class="lv-n">{n}</span><h3>{W(h)}</h3>{P(t)}</li>' for n,h,t in LEVERS)}</ol>
    <div class="cost-b">
      <div class="sim rv">
        <p class="sim-k">原価率が下がると、粗利はどれだけ増えるか</p>
        <div class="tw"><table><thead><tr><th></th><th>1ポイント</th><th>2ポイント</th><th>3ポイント</th></tr></thead><tbody>{sim_rows()}</tbody></table></div>
        <p class="sim-n">{W('年間の|粗利の|増加額（単純計算）。|年商6億円の|会社で|原価率が|2ポイント|下がれば、|粗利は|年1,200万円|増えます。')}</p>
      </div>
      <div class="notdo rv">
        <p class="nd-k">原価を下げるために、やらないこと</p>
        <ul>{''.join(f'<li>{W(x)}</li>' for x in NOT_DO)}</ul>
        {P('協力業者さんとの発注条件・支払条件は、グループ入り後もこれまでどおりです。腕の良い職人さんに選ばれ続けることが、長い目で見て一番の原価対策だと考えています。')}
      </div>
    </div>
  </div>
</section>"""
TOPCOST=f"""<section class="tcost dark">
  <div class="w">
    <div class="tc-l rv">
      <p class="sh-en" aria-hidden="true">Cost</p><p class="sh-ja">原価の改善</p>
      <h2>{W('利益は、|売上より先に|原価で|決まる。')}</h2>
      {P('住設・建材の共同購買、購入単価の見える化、着工前の実行予算。グループの規模を使って「買い方」と「段取り」を変え、粗利を残します。協力業者さんの単価を下げることはしません。')}
      <a class="btn btn-white" href="service.html#cost"{NT}>原価改善の進め方を見る {AR}</a>
    </div>
    <div class="tc-r rv">
      <p class="tc-k">年商6億円の会社で、原価率が</p>
      <ul>
        <li><span>1ポイント下がると</span><b>+600<small>万円</small></b></li>
        <li><span>2ポイント下がると</span><b>+1,200<small>万円</small></b></li>
        <li><span>3ポイント下がると</span><b>+1,800<small>万円</small></b></li>
      </ul>
      <p class="tc-n">年間の粗利増加額（単純計算）</p>
    </div>
  </div>
</section>"""

# ---------- cases ----------
CASES=[
 dict(slug='case-1',tag='後継者不在',en='Succession',pid='TJ4CndIc9z8',alt='地方都市の住宅街',
  title='子どもは|別の道へ。|社員に|継がせるには|資金が|足りない。',
  short='株式はグループが引き受け、経営は番頭格の社員が継ぐ。所有と経営を分けて、社内承継を実現した想定例です。',
  prof=[('エリア','地方都市'),('事業','注文住宅・リフォーム'),('規模','年商 約8億円／年間引渡し 25棟'),('社員','18名'),('社長','68歳・創業者')],
  before=['長男は県外で会社員。家業を継ぐ意思はない','番頭格の工事部長（52歳）に継がせたいが、株式を買い取る資金を用意できない','社長個人が、会社の借入 約3億円の連帯保証を負っている','引き渡したOB施主様 約600棟の定期点検が、今後も続く'],
  trigger='取引銀行との面談で事業承継が話題に上ったことをきっかけに、仲介会社経由でご相談いただきました。ご希望は「会社を残すこと」と「部長を社長にすること」の両立でした。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','2年間、代表権のない会長として残留'),('次の社長','工事部長が1年目に取締役、3年目に代表取締役へ'),('社名・屋号','変更なし'),('雇用・給与','全員継続。給与体系も変更なし'),('個人保証','クロージング時に金融機関と協議し、解除'),('期間','初回面談からクロージングまで 約7ヶ月')],
  steps=[('Day 1','社長と私たちで、全社員に直接ご説明'),('30 days','月次決算をグループ本部で締める体制へ移行'),('100 days','部長を交えた経営会議を毎月開催。実行予算の管理を開始'),('1 year','部長が取締役に就任。現場監督を2名採用')],
  change=[('月次の数字','年1回の決算のみ','翌月10日に確定'),('社長の個人保証','約3億円','解除'),('次の社長','未定','社内の工事部長に決定')],
  voice='一番怖かったのは、社員に「売られた」と思われることでした。説明の場に一緒に立ってもらえたのが大きかった。',
  point='社内承継の一番の壁は、株式を買い取る資金です。グループが株式を引き受け、経営は社員が継ぐ形にすれば、資金の問題と「誰が継ぐか」の問題を切り分けられます。'),
 dict(slug='case-2',tag='成長の壁',en='Growth',pid='4UVtFIfK1eo',alt='木造の骨組み',
  title='受注は|あるのに、|人が|採れず|年20棟から|伸びない。',
  short='社長は続投し、株式の一部も持ち続ける。採用・集客・管理部門をグループで支え、社長が営業と現場に戻った想定例です。',
  prof=[('エリア','首都圏郊外'),('事業','注文住宅'),('規模','年商 約6億円／年間引渡し 20棟'),('社員','14名'),('社長','55歳・二代目')],
  before=['受注残はあるが、現場監督が2名で年20棟が上限','求人を出しても、応募は年に数件','社長が営業・設計確認・経理まで一人で兼任','Web集客は外注任せで、成果が数字で見えていない'],
  trigger='「会社を売りたい」ではなく、「伸ばすための仲間がほしい」というご相談でした。社長の続投を前提に検討を進めました。',
  scheme=[('取得する株式','70%（社長が30%を継続保有）'),('社長の処遇','代表取締役として続投'),('社名・屋号','変更なし'),('雇用・給与','全員継続'),('個人保証','借り換えにあわせて段階的に解除'),('期間','初回面談からクロージングまで 約5ヶ月')],
  steps=[('Day 1','社長と私たちで、全社員に直接ご説明'),('30 days','問い合わせ数・来場数・成約率を、グループ共通の管理表に統一'),('100 days','グループ合同採用で、現場監督と設計の募集を開始'),('1 year','現場監督4名体制へ。経理・総務はグループ本部が担当')],
  change=[('現場監督','2名','4名'),('年間引渡し','20棟','28棟（目標）'),('社長の事務作業','週 約15時間','週 約2時間')],
  voice='社長を続けられるなら、という条件で話を聞きました。営業と現場に戻れたのが何よりです。',
  point='成長期の会社に足りないのは、資金より「人と仕組み」です。株式の一部を持ち続けてもらうことで、社長と私たちが同じ方向を向いて会社を伸ばせます。'),
 dict(slug='case-3',tag='廃業の検討',en='Continuity',pid='q1tyQip5AQQ',alt='大きな窓のある室内',
  title='体力的に|限界。|でも|施主様の|アフターだけは|残したい。',
  short='社名とアフター窓口を残し、近隣のグループ会社と管理部門・仕入れを共通化。社長は半年で引退した想定例です。',
  prof=[('エリア','地方の郡部'),('事業','リフォーム中心'),('規模','年商 約3億円'),('社員','6名'),('社長','72歳・創業者')],
  before=['体力的に限界で、後継者はいない','廃業すると、OB施主様 約1,200件のアフターの行き先がなくなる','建設業許可の経営業務の管理責任者が、社長しかいない','債務超過ではないが、利益はほぼゼロ'],
  trigger='廃業の手続きを相談していた顧問税理士からのご紹介です。「OB施主さんのアフターだけは残したい」というお話から始まりました。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','半年で引退。その後は非常勤の相談役'),('社名・アフター窓口','変更なし'),('建設業許可','要件を満たす人材をグループから役員として迎え、許可を維持'),('管理部門','近隣のグループ会社と経理・発注を共通化'),('期間','初回面談からクロージングまで 約5ヶ月')],
  steps=[('Day 1','社長と私たちで、全社員に直接ご説明'),('30 days','OB施主様へ、点検の窓口と担当者が変わらないことをご案内'),('100 days','近隣のグループ会社と、発注・経理を共通化'),('1 year','社長が相談役へ。現場責任者を中心とした体制に移行')],
  change=[('営業利益','ほぼゼロ','黒字化（目標）'),('OB施主様の窓口','廃業で失われる可能性','継続'),('資材の発注','社長個人の付き合いで分散','グループの共同購買')],
  voice='やめる以外に道はないと思っていました。電話番号も担当者もそのままで、お客さんに迷惑をかけずに済みました。',
  point='規模が小さく利益が薄くても、OB施主様というストックと地域の信用には価値があります。管理部門と仕入れを近くのグループ会社と分け合えば、1社では難しかった採算が合うようになります。'),
 dict(slug='case-4',tag='粗利の低下',en='Cost',pid='pcYN7Pi8_BQ',alt='夕暮れの住宅街',
  title='資材は|上がり、|粗利は|3年で|5ポイント|下がった。',
  short='職人さんの単価には手を付けず、発注の集約と実行予算の徹底で粗利を立て直してから承継する想定例です。',
  prof=[('エリア','中核市'),('事業','注文住宅・分譲'),('規模','年商 約10億円／年間引渡し 35棟'),('社員','24名'),('社長','62歳・二代目')],
  before=['資材価格の上昇を販売価格に転嫁しきれず、粗利率が3年で約5ポイント低下','発注は担当者ごとにばらばら。同じ住設を、現場ごとに違う価格で購入','実行予算を組まずに着工し、赤字の現場が引き渡し後に判明','後継者候補はいるが、業績の悪化で承継に踏み切れない'],
  trigger='「数字が見えないまま、次の社長に会社を渡すわけにはいかない」。承継の前に、立て直しも一緒に進めたいというご相談でした。',
  scheme=[('取得する株式','100%（株式譲渡）'),('社長の処遇','2年間続投し、その後は社内の後継者へ'),('社名・屋号','変更なし'),('雇用・給与','全員継続'),('協力業者さん','発注条件・支払条件は変更なし'),('期間','初回面談からクロージングまで 約6ヶ月')],
  steps=[('Day 1','社長と私たちで、全社員に直接ご説明'),('30 days','過去2年の全現場の原価を洗い出し、品目別の購入単価を一覧化'),('100 days','住設・建材をグループの共同購買に切り替え。着工前の実行予算を必須に'),('1 year','標準仕様を整理し、図面チェックの様式を統一して手戻りを削減')],
  change=[('実行予算','一部の現場のみ','全現場で着工前に作成'),('住設・建材の購入先','担当者ごとに分散','グループの共同購買に集約'),('粗利率','3年で約5ポイント低下','2ポイント改善が目標（粗利 年約2,000万円）')],
  voice='職人さんの単価には手を付けない、と最初に言ってもらえたので、協力業者さんにも説明しやすかった。',
  point='原価は「誰かの単価を叩く」より、「ばらばらの発注を揃える」「着工前に数字を決める」ほうが大きく下がります。立て直してから承継すれば、次の社長の負担も軽くなります。'),
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
    {head('Process','ご相談から引き継ぎまで','6つの|ステップで、|通常は|半年|ほどです','急いで決めていただく必要はありません。各段階で、何をして、何をご用意いただき、誰にまで話が伝わるのかを先にお伝えします。')}
    {gantt()}
    <ol class="fsteps">{''.join(f'''<li class="rv"><div class="fs-h"><span class="fs-n">STEP {i+1:02d}</span><p class="fs-en">{e}</p><h3>{W(h)}</h3><p class="fs-t">期間の目安　{t}</p></div><div class="fs-b">{P(d)}<div class="fs-m"><div><p class="fs-k">ご用意いただくもの</p><ul>{''.join(f'<li>{x}</li>' for x in prep)}</ul></div><div><p class="fs-k">話が伝わる範囲</p><p class="fs-who">{who}</p></div></div></div></li>''' for i,(h,e,t,d,prep,who) in enumerate(FSTEPS))}</ol>
  </div>
</section>"""
SECRET=f"""<section class="secret dark">
  <div class="w">
    {head('Confidential','秘密を守るために','ご相談の|事実は、|社員にも|取引先にも|伝わりません')}
    <ul class="sc-l">{''.join(f'<li class="rv"><span>{n}</span><h3>{W(h)}</h3>{P(t)}</li>' for n,h,t in [('01','面談は社外か|オンラインで','会社に伺うことはありません。ご自宅の近く、私たちの事務所、またはオンラインで行います。'),('02','連絡方法は|事前に決める','郵送物や電話は、社長と決めた方法でのみご連絡します。会社の代表番号にお電話することはありません。'),('03','秘密保持契約は|初回から','ご希望があれば、初回の面談の前に秘密保持契約を結びます。')])}</ul>
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
SVC_KPI=kpis([('6','領域','グループで|支える|仕事'),('100','日','引き継ぎの|計画'),('30','年','保有を|前提に|経営'),('0','円','ご相談の|費用')])
COMPANY_BAND=band('-MVSfkR4xz4','Our stance','社名も、|社員も、|施主様との|約束も。','引き継ぐのは、株式だけではありません。')
SERVICE_BAND=band('pcYN7Pi8_BQ','Cost','職人さんの|手間賃ではなく、|ムダな発注を|減らす。','原価の改善は、協力業者さんに選ばれ続けることとセットで考えます。')
CASES_BAND=band('Q6sCJFHCubc','Your case','同じ会社は、|ひとつも|ありません。','事例と違う状況でも、まずはお話を伺います。')
FLOW_BAND=band('a8A-z_ZPEC0','No rush','決めるのは、|社長です。','どの段階でも、立ち止まったり、お断りいただいたりして構いません。')
