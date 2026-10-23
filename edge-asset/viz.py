# on-brand diagrams for the support rows (service page), drawn as inline SVG instead of stock photos
NAVY,BLUE,SKY,LINE='#0c2747','#2268c8','#7fb0ff','rgba(255,255,255,.12)'
def _svg(label,ja,body,foot):
    grid=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="400" stroke="{LINE}"/>' for x in (150,300,450))
    return (f'<svg viewBox="0 0 600 400" role="img" aria-label="{ja}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="600" height="400" fill="{NAVY}"/>{grid}'
            f'<text x="36" y="48" class="vz-en">{label}</text><text x="36" y="72" class="vz-ja">{ja}</text>'
            f'{body}<line x1="36" y1="348" x2="564" y2="348" stroke="rgba(255,255,255,.25)"/>'
            f'<text x="36" y="376" class="vz-f">{foot}</text></svg>')

def viz_marketing():
    rows=[('反響',100,'100'),('来場',42,'42'),('商談',22,'22'),('契約',8,'8')]
    b=''
    for i,(k,w,v) in enumerate(rows):
        y=110+i*52; ww=w/100*420
        b+=(f'<text x="36" y="{y+25}" class="vz-k">{k}</text>'
            f'<rect x="104" y="{y}" width="{ww:.0f}" height="36" fill="{BLUE if i<3 else SKY}" opacity="{1-i*.18:.2f}"/>'
            f'<text x="{104+ww+12:.0f}" y="{y+25}" class="vz-v">{v}</text>')
    return _svg('LEAD FUNNEL','反響から契約までを毎月計測',b,'広告費 ÷ 反響数＝反響単価。媒体ごとに比べて予算を配分（数値は例）')

def viz_recruiting():
    b=''
    roles={3:BLUE,8:BLUE,12:SKY,17:BLUE,21:SKY,26:'#ffffff',30:BLUE,34:'#ffffff',39:SKY}
    for i in range(40):
        cx=56+(i%10)*28; cy=118+(i//10)*36
        c=roles.get(i)
        b+=f'<circle cx="{cx}" cy="{cy}" r="8" fill="{c or "none"}" stroke="{c or "rgba(255,255,255,.3)"}"/>'
    for j,(t,c) in enumerate([('設計',BLUE),('現場監督',SKY),('大工','#ffffff')]):
        b+=f'<circle cx="{62+j*92}" cy="276" r="6" fill="{c}"/><text x="{74+j*92}" y="281" class="vz-s">{t}</text>'
    for j,t in enumerate(['A社','B社','C社']):
        y=118+j*64
        b+=(f'<path d="M340 {172} C 400 {172}, 410 {y+20}, 450 {y+20}" fill="none" stroke="{SKY}" stroke-width="1.5" opacity=".7"/>'
            f'<rect x="452" y="{y}" width="112" height="40" fill="none" stroke="rgba(255,255,255,.55)"/>'
            f'<text x="508" y="{y+26}" text-anchor="middle" class="vz-b">{t}</text>')
    return _svg('GROUP HIRING','グループ合同で採用し、各社へ配属',b,'一社では出せない規模の求人で、応募の母数を増やす')

def viz_finance():
    bud=[52,58,64,70,74,80,78,84,90,94,98,104]
    act=[48,60,66,68,78,84,80,90,96,92,104,112]
    b=''
    for i,(p,a) in enumerate(zip(bud,act)):
        x=48+i*42
        b+=(f'<rect x="{x}" y="{320-p*1.8:.0f}" width="26" height="{p*1.8:.0f}" fill="none" stroke="rgba(255,255,255,.35)"/>'
            f'<rect x="{x+5}" y="{320-a*1.8:.0f}" width="16" height="{a*1.8:.0f}" fill="{BLUE if a>=p else SKY}"/>'
            f'<text x="{x+13}" y="338" text-anchor="middle" class="vz-m">{(i+3)%12+1}</text>')
    b+=(f'<rect x="372" y="96" width="12" height="12" fill="none" stroke="rgba(255,255,255,.5)"/><text x="390" y="107" class="vz-s">予算</text>'
        f'<rect x="440" y="96" width="12" height="12" fill="{BLUE}"/><text x="458" y="107" class="vz-s">実績</text>')
    return _svg('MONTHLY P&amp;L','月次決算で、予算と実績を毎月比べる',b,'翌月10日に数字を確定。ずれた月は、その場で原因と打ち手を決める（数値は例）')

def viz_operations():
    b=''
    for j,t in enumerate(['A社','B社','C社']):
        y=104+j*74
        b+=(f'<rect x="36" y="{y}" width="104" height="44" fill="none" stroke="rgba(255,255,255,.55)"/><text x="88" y="{y+28}" text-anchor="middle" class="vz-b">{t}</text>'
            f'<line x1="140" y1="{y+22}" x2="236" y2="200" stroke="{SKY}" stroke-width="1.5" opacity=".7"/>')
    b+=(f'<circle cx="300" cy="200" r="66" fill="{BLUE}"/><circle cx="300" cy="200" r="82" fill="none" stroke="{SKY}" stroke-dasharray="3 6"/>'
        f'<text x="300" y="194" text-anchor="middle" class="vz-c">グループ本部</text><text x="300" y="218" text-anchor="middle" class="vz-cs">共同購買</text>')
    for j,t in enumerate(['メーカー','商社','プレカット']):
        y=104+j*74
        b+=(f'<line x1="364" y1="200" x2="460" y2="{y+22}" stroke="{SKY}" stroke-width="1.5" opacity=".7"/>'
            f'<rect x="460" y="{y}" width="104" height="44" fill="#ffffff"/><text x="512" y="{y+28}" text-anchor="middle" class="vz-bn">{t}</text>')
    return _svg('GROUP PURCHASING','各社の発注を、本部でまとめる',b,'発注量をまとめて交渉し、1社では届かない条件を引き出す')

VIZ={'MARKETING':viz_marketing(),'RECRUITING':viz_recruiting(),'FINANCE':viz_finance(),'OPERATIONS':viz_operations()}
