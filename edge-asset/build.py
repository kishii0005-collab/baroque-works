import sys
U=lambda i,w=0:f'https://unsplash.com/photos/{i}/download?force=true&amp;w=1800'  # one size per photo so the browser fetches it only once
SAFE=U('Q6sCJFHCubc',2000)
import os
IMG_DIR=os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),'img')
BACKUP=['Q6sCJFHCubc','rD28m9BmXVs','4UVtFIfK1eo']
def src_list(i):
    # a photo saved in edge-asset/img/ always wins; otherwise load it from Unsplash
    local=f'img/{i}.jpg'
    out=[local] if os.path.exists(os.path.join(IMG_DIR,f'{i}.jpg')) else []
    # via the wsrv.nl image cache first (fetched once on their side, then served from cache), then Unsplash directly
    from urllib.parse import quote
    proxied='https://wsrv.nl/?url='+quote(f'unsplash.com/photos/{i}/download?force=true&w=1800',safe='')+'&amp;w=1800&amp;q=82&amp;output=jpg'
    return out+[U(i),proxied]
def img(i,alt='',w=1400,lazy=True,fb=None):
    chain=[]
    for x in [i]+[y for y in (fb or [])+BACKUP if y!=i]:
        chain+=src_list(x)
    return (f'<img src="{chain[0]}" alt="{alt}"{" loading=\"lazy\"" if lazy else ""} data-fb="{"|".join(chain[1:5])}" onerror="var l=(this.dataset.fb||\'\').split(\'|\').filter(Boolean);if(l.length){{this.dataset.fb=l.slice(1).join(\'|\');this.src=l[0]}}else{{this.onerror=null;this.style.visibility=\'hidden\';this.parentNode.classList.add(\'noimg\')}}">')
W=lambda t:t.replace('|','<wbr>')
def nb(t,n=9):  # keep the last phrase together; the break lands right after a particle or comma
    if len(t)<=n+3: return t
    i=len(t)-n
    while i>len(t)-16 and t[i-1] not in 'をにはがのでとも、': i-=1
    if t[i-1] not in 'をにはがのでとも、': i=len(t)-n
    return t[:i]+f'<span class="nb">{t[i:]}</span>'
def P(t,cls=''):
    c=f' class="{cls}"' if cls else ''
    return f'<p{c}>{nb(t)}</p>'
def head(en,ja,h2,lead='',center=False):
    l=f'<div class="sh-lead">{P(lead)}</div>' if lead else ''
    return f'''<header class="sh{' c' if center else ''}"><div class="sh-t"><p class="sh-en" aria-hidden="true">{en}</p><p class="sh-ja">{ja}</p><h2>{W(h2)}</h2></div>{l}</header>'''

CSS=r'''
/* layout: editorial corporate — asymmetric grid, edge-bleeding photos, big English section titles; navy + one bright blue */
:root{
  --bg:#ffffff;
  --mist:#f1f4f8;
  --ink:#16202c;
  --ink-2:#4a5565;
  --mute:#8a94a3;
  --line:#d9e0e8;
  --navy:#0c2747;
  --blue:#2268c8;
  --en:"Jost","Helvetica Neue",Arial,sans-serif;
  --fh:"Zen Kaku Gothic New","Noto Sans JP","Hiragino Kaku Gothic ProN",sans-serif;
  --f:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
  --gut:max(48px,env(safe-area-inset-left,0px));
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f);font-size:15.5px;line-height:2.05;letter-spacing:.05em;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{display:block;width:100%;height:100%;object-fit:cover;color:transparent;font-size:0}
p{margin:0 0 1.3em}
h1,h2,h3,h4{margin:0;font-family:var(--fh);font-weight:700}
h1,h2,h3,h4,.catch,.lede,.big,.open li,.open .note,summary span{word-break:keep-all;overflow-wrap:anywhere;line-break:strict}
summary span{word-break:normal}
.nb{white-space:nowrap}
.w{width:100%;max-width:1240px;margin:0 auto;padding-left:var(--gut);padding-right:max(48px,env(safe-area-inset-right,0px))}
@media (max-width:760px){body{font-size:15px;line-height:1.95}:root{--gut:max(22px,env(safe-area-inset-left,0px))}.w{padding-right:max(22px,env(safe-area-inset-right,0px))}}
:focus-visible{outline:2px solid var(--blue);outline-offset:3px}
.ph{position:relative;overflow:hidden;background:#cfd8e3}
.ph.noimg{background:linear-gradient(135deg,#1b3d6b,#0c2747)}
.ph.noimg::after{content:"EDGE ASSET";position:absolute;inset:0;display:grid;place-items:center;font-family:var(--en);letter-spacing:.3em;font-size:12px;color:rgba(255,255,255,.35)}
section{padding-block:140px}
@media (max-width:760px){section{padding-block:84px}}

/* section head */
.sh{display:grid;grid-template-columns:1fr 1fr;gap:28px 72px;align-items:end;margin-bottom:72px}
.sh-en{font-family:var(--en);font-weight:300;font-size:clamp(56px,7.2vw,104px);line-height:.9;letter-spacing:-.01em;color:var(--navy);margin:0 0 26px}
.sh-ja{font-size:13px;font-weight:500;color:var(--blue);margin:0 0 14px;display:flex;align-items:center;gap:12px}
.sh-ja::before{content:"";width:8px;height:8px;background:var(--blue)}
.sh h2{font-size:clamp(22px,2.3vw,30px);line-height:1.7;letter-spacing:.06em}
.sh-lead p{margin:0;color:var(--ink-2)}
.sh.c{grid-template-columns:1fr;text-align:center}.sh.c .sh-ja{justify-content:center}.sh.c .sh-lead{max-width:40em;margin:0 auto}
.dark .sh-en{color:#fff}.dark .sh-ja{color:#8fb6ec}.dark .sh-ja::before{background:#8fb6ec}.dark .sh-lead p{color:#b6c3d4}
/* heads placed inside a column take the full column */
.grid .sh{grid-template-columns:1fr;margin-bottom:36px}
.grid .sh .sh-lead{margin-top:-8px}
@media (max-width:860px){.sh{grid-template-columns:1fr;margin-bottom:48px}.sh-en{font-size:52px;margin-bottom:18px}.sh h2{font-size:21px}.sh.c{text-align:left}.sh.c .sh-ja{justify-content:flex-start}}

/* buttons / links */
.btn{display:inline-flex;align-items:center;justify-content:space-between;gap:36px;min-width:260px;padding:20px 26px 20px 30px;font-family:inherit;font-size:14.5px;font-weight:500;letter-spacing:.1em;line-height:1.4;border:1px solid transparent;cursor:pointer;transition:background .3s,color .3s,border-color .3s}
.btn .ar{width:22px;height:1px;background:currentColor;position:relative;transition:width .3s}
.btn .ar::after{content:"";position:absolute;right:0;top:-3px;width:7px;height:7px;border-top:1px solid currentColor;border-right:1px solid currentColor;transform:rotate(45deg)}
.btn:hover .ar{width:32px}
.btn-navy{background:var(--navy);color:#fff}.btn-navy:hover{background:var(--blue)}
.btn-blue{background:var(--blue);color:#fff}.btn-blue:hover{background:var(--navy)}
.btn-white{background:#fff;color:var(--navy)}.btn-white:hover{background:var(--mist)}
.btn-ghost{border-color:rgba(255,255,255,.65);color:#fff}.btn-ghost:hover{background:#fff;color:var(--navy)}
.btn-line{border-color:var(--navy);color:var(--navy)}.btn-line:hover{background:var(--navy);color:#fff}
.btns{display:flex;flex-wrap:wrap;gap:14px}
.tl{display:inline-flex;align-items:center;gap:16px;font-size:14px;font-weight:500;color:var(--navy);padding-bottom:8px;border-bottom:1px solid var(--navy)}
.tl .ar{width:22px;height:1px;background:currentColor;position:relative}
.tl .ar::after{content:"";position:absolute;right:0;top:-3px;width:7px;height:7px;border-top:1px solid currentColor;border-right:1px solid currentColor;transform:rotate(45deg)}
@media (max-width:760px){.btns{flex-direction:column}.btn{width:100%;min-width:0}}

/* header */
header.site{position:absolute;inset:0 0 auto;z-index:20;color:#fff}
header.site .w{max-width:none;display:flex;align-items:center;justify-content:space-between;height:100px;gap:24px}
.logo{display:flex;align-items:center;gap:14px}
.logo svg{width:34px;height:34px}
.logo b{display:block;font-family:var(--en);font-weight:500;font-size:20px;letter-spacing:.24em;line-height:1.1}
.logo small{display:block;font-size:10px;letter-spacing:.2em;opacity:.8;margin-top:3px}
.gnav{display:flex;align-items:center;gap:32px;font-size:13px;font-weight:500}
.gnav a.nl{position:relative;padding:4px 0}
.gnav a.nl::after{content:"";position:absolute;left:0;right:100%;bottom:0;height:1px;background:currentColor;transition:right .3s}
.gnav a.nl:hover::after{right:0}
.gnav .tel{font-family:var(--en);font-size:20px;letter-spacing:.06em;line-height:1.2;text-align:right}
.gnav .tel small{display:block;font-family:var(--f);font-size:10px;opacity:.8;letter-spacing:.1em}
.gnav .btn{min-width:0;padding:14px 22px;gap:18px;font-size:13px}
@media (max-width:1200px){.gnav a.nl{display:none}}
@media (max-width:760px){header.site .w{height:70px}.gnav .tel{display:none}.gnav .btn{padding:10px 14px;font-size:12px;gap:10px}.gnav .btn .ar{display:none}.logo b{font-size:16px}.logo svg{width:28px;height:28px}}

/* hero */
.hero{position:relative;height:100vh;height:100svh;min-height:640px;max-height:1080px;color:#fff;overflow:hidden;padding:0;background:var(--navy)}
.slide{position:absolute;inset:0;opacity:0;transition:opacity 1.6s ease}
.slide.on{opacity:1}
.slide img{transform:scale(1.08)}
.slide.on img{animation:zoom 9s linear forwards}
@keyframes zoom{to{transform:scale(1)}}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(8,24,46,.8) 0%,rgba(8,24,46,.25) 50%,rgba(8,24,46,.35) 100%);pointer-events:none}
.hero .copy{position:absolute;z-index:2;left:0;right:0;bottom:150px}
.hero .copy .w{max-width:none}
.hero .en{font-family:var(--en);font-weight:300;font-size:13px;letter-spacing:.3em;margin:0 0 28px;opacity:.9}
.hero h1{font-size:clamp(32px,4.6vw,64px);line-height:1.5;letter-spacing:.08em;margin:0 0 28px;max-width:15em;font-weight:700}
.hero .lead{font-size:15px;max-width:36em;opacity:.92;margin:0 0 40px}
.news{position:absolute;z-index:3;left:0;right:0;bottom:0;background:rgba(8,24,46,.55);backdrop-filter:blur(4px);border-top:1px solid rgba(255,255,255,.15)}
.news .w{max-width:none;display:flex;align-items:center;gap:28px;height:68px;font-size:13px}
.news b{font-family:var(--en);font-weight:500;letter-spacing:.2em;font-size:12px}
.news time{font-family:var(--en);opacity:.8}
.news .t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pager{display:flex;align-items:center;gap:14px;font-family:var(--en);font-size:12px}
.pager button{width:36px;height:2px;padding:0;border:0;background:rgba(255,255,255,.3);cursor:pointer;position:relative;overflow:hidden}
.pager button::after{content:"";position:absolute;inset:0;background:#fff;transform:scaleX(0);transform-origin:left}
.pager button.on::after{animation:fill 6s linear forwards}
@keyframes fill{to{transform:scaleX(1)}}
@media (max-width:760px){.hero{min-height:620px}.hero .copy{bottom:120px}.hero .en{font-size:9.5px;letter-spacing:.18em;margin-bottom:18px}.hero h1{font-size:28px;line-height:1.55}.hero .lead{font-size:13.5px;margin-bottom:28px}.news .w{height:auto;padding-block:14px;flex-wrap:wrap;gap:6px 14px}.news .t{flex-basis:100%}.pager{display:none}}

/* about: text + bleeding photo stack */
.about{position:relative;overflow:hidden}
.about .grid{display:grid;grid-template-columns:5fr 6fr;gap:80px;align-items:center}
.about .catch{font-family:var(--fh);font-weight:700;font-size:clamp(24px,2.6vw,34px);line-height:1.8;letter-spacing:.08em;margin:0 0 40px}
.about .body p{color:var(--ink-2)}
.about .pics{position:relative;height:620px;margin-right:calc(-1 * max(48px,(100vw - 1240px)/2 + 48px))}
.about .pics .ph{position:absolute}
.about .p1{right:0;top:0;width:82%;height:72%}
.about .p2{left:0;bottom:0;width:44%;height:46%;outline:12px solid #fff}
.bgword{position:absolute;left:-1vw;bottom:-2.4vw;font-family:var(--en);font-weight:500;font-size:15vw;line-height:1;color:var(--mist);z-index:-1;white-space:nowrap;letter-spacing:-.02em;pointer-events:none}
@media (max-width:960px){.about .grid{grid-template-columns:1fr;gap:56px}.about .pics{height:420px;margin-right:calc(-1 * var(--gut))}}
@media (max-width:760px){.about .catch{font-size:23px}.about .pics{height:320px}.about .p2{outline-width:6px}}

/* market (dark, photo right) */
.market{background:var(--navy);color:#fff;position:relative;overflow:hidden}
.market .grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.market .num{display:flex;align-items:center;gap:28px;padding:34px 0;border-top:1px solid rgba(255,255,255,.2)}
.market .num:last-of-type{border-bottom:1px solid rgba(255,255,255,.2)}
.market .num strong{font-family:var(--en);font-weight:300;font-size:clamp(68px,7.5vw,110px);line-height:.85;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.market .num strong small{font-size:.32em;margin-left:6px}
.market .num h3{font-size:16px;margin:0 0 4px}
.market .num p{margin:0;font-size:13.5px;color:#b6c3d4;line-height:1.8}
.market .src{font-size:12px;color:#8a9ab0;margin-top:20px}
.market .ph{aspect-ratio:4/5}
@media (max-width:960px){.market .grid{grid-template-columns:1fr;gap:56px}.market .ph{aspect-ratio:16/10}}
@media (max-width:560px){.market .num{flex-direction:column;align-items:flex-start;gap:14px}.market .num strong{font-size:72px}}

/* gallery strip */
.strip{padding:0;display:grid;grid-template-columns:2fr 1fr 1.4fr 1fr;height:380px;gap:0}
.strip .ph{height:100%}
@media (max-width:760px){.strip{grid-template-columns:1fr 1fr;height:auto}.strip .ph{height:170px}}

/* stance */
.stance{position:relative;color:#fff;overflow:hidden;padding-block:200px}
.stance>.ph{position:absolute;inset:0}
.stance::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,24,46,.85),rgba(8,24,46,.45));z-index:1}
.stance .w{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:end}
.stance .big{white-space:nowrap;font-family:var(--fh);font-weight:700;font-size:clamp(52px,6.4vw,96px);line-height:1.1;letter-spacing:.1em;margin:0}
.stance p{color:rgba(255,255,255,.9)}
@media (max-width:860px){.stance{padding-block:110px}.stance .w{grid-template-columns:1fr;gap:28px}.stance .big{font-size:54px}}

/* message */
.msg .grid{display:grid;grid-template-columns:5fr 6fr;gap:96px;align-items:start}
.msg .ph{aspect-ratio:4/5}
.msg .ph span{position:absolute;left:0;bottom:0;background:#fff;font-size:11px;padding:8px 14px 0 0;color:var(--mute)}
.msg .who{display:flex;align-items:baseline;gap:18px;margin-top:24px}
.msg .who small{font-size:12px;color:var(--mute)}
.msg .who b{font-family:var(--fh);font-size:22px;letter-spacing:.24em}
.msg ul{list-style:none;padding:0;margin:14px 0 0;font-size:13.5px;color:var(--ink-2)}
.msg li{padding:10px 0;border-top:1px solid var(--line)}
.msg .letter .lede{font-family:var(--fh);font-weight:700;font-size:clamp(22px,2.2vw,28px);line-height:1.8;letter-spacing:.06em;margin:0 0 40px}
.msg .letter p{color:var(--ink-2)}
.msg .sign{margin-top:36px;text-align:right;font-family:var(--fh);font-size:15px;color:var(--ink)}
@media (max-width:960px){.msg .grid{grid-template-columns:1fr;gap:48px}.msg .ph{max-width:400px}}

/* promise: numbered two-column list */
.promise{background:var(--mist)}
.plist{display:grid;grid-template-columns:1fr 1fr;column-gap:72px}
.pi{display:grid;grid-template-columns:76px 1fr;align-content:start;gap:4px 20px;padding:34px 0;border-top:1px solid var(--line)}
.pi .n{font-family:var(--en);font-weight:300;font-size:44px;line-height:1;color:var(--blue);grid-row:span 2}
.pi h3{font-size:18.5px;line-height:1.6;letter-spacing:.05em}
.pi p{margin:0;color:var(--ink-2);font-size:14.5px}
.pi.ask{background:#fff;border-top:0;padding:30px 30px 26px;margin-top:20px;grid-template-columns:1fr}
.pi.ask h3{font-size:16px;color:var(--navy);margin-bottom:10px}
.pi.ask ul{margin:0;padding:0;list-style:none;font-size:14px;color:var(--ink-2)}
.pi.ask li{padding:6px 0 6px 18px;position:relative}
.pi.ask li::before{content:"";position:absolute;left:0;top:19px;width:8px;height:1px;background:var(--ink-2)}
@media (max-width:860px){.plist{grid-template-columns:1fr}.pi{grid-template-columns:56px 1fr;padding:26px 0}.pi .n{font-size:34px}}

/* cta band */
.cta{position:relative;color:#fff;overflow:hidden;padding-block:120px}
.cta>.ph{position:absolute;inset:0}
.cta::before{content:"";position:absolute;inset:0;background:rgba(12,39,71,.82);z-index:1}
.cta .w{position:relative;z-index:2;display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center}
.cta h2{font-size:clamp(22px,2.6vw,34px);line-height:1.7;letter-spacing:.06em;margin-bottom:14px}
.cta p{margin:0;color:rgba(255,255,255,.85)}
.cta .tel{margin-top:22px;font-size:13px}
.cta .tel b{font-family:var(--en);font-weight:400;font-size:30px;letter-spacing:.04em;margin-left:12px;white-space:nowrap}
@media (max-width:560px){.cta .tel b{display:block;margin:4px 0 0}}
.cta .btns{flex-direction:column;align-items:flex-end}
@media (max-width:860px){.cta{padding-block:84px}.cta .w{grid-template-columns:1fr}.cta .btns{align-items:stretch}}

/* support: alternating rows */
.row{display:grid;grid-template-columns:1fr 1fr;gap:0;align-items:center;margin-bottom:56px}
.row .ph{aspect-ratio:3/2}
.row .frame{min-width:0}
.row .tx{padding:0 0 0 72px}
.row:nth-child(even) .frame{order:2}
.row:nth-child(even) .tx{padding:0 72px 0 0}
.row .n{font-family:var(--en);font-weight:300;font-size:15px;letter-spacing:.2em;color:var(--blue);display:flex;align-items:center;gap:14px;margin-bottom:12px}
.row .n::after{content:"";width:48px;height:1px;background:var(--blue)}
.row h3{font-size:clamp(20px,2vw,26px);letter-spacing:.08em;margin-bottom:16px}
.row p{color:var(--ink-2)}
.row dl{margin:0;font-size:13.5px;border-top:1px solid var(--line)}
.row dl div{display:grid;grid-template-columns:8em 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}
.row dt{color:var(--navy);font-weight:500}
.row dd{margin:0;color:var(--ink-2)}
@media (max-width:860px){.row{grid-template-columns:1fr;margin-bottom:56px}.row .tx,.row:nth-child(even) .tx{padding:28px 0 0}.row:nth-child(even) .frame{order:0}.row dl div{grid-template-columns:1fr;gap:0}}

/* people: one wide photo, four columns */
.people{background:var(--mist)}
.people .ph{height:420px;margin-bottom:56px}
.pg{display:grid;grid-template-columns:repeat(4,1fr);gap:0 40px}
.pg article{border-top:2px solid var(--navy);padding-top:22px}
.pg .who{font-size:12.5px;font-weight:500;color:var(--blue);margin:0 0 10px}
.pg h3{font-size:17px;line-height:1.7;margin-bottom:12px}
.pg p{margin:0;font-size:14px;color:var(--ink-2)}
@media (max-width:1000px){.pg{grid-template-columns:1fr 1fr;gap:40px 32px}.people .ph{height:300px}}
@media (max-width:560px){.pg{grid-template-columns:1fr;gap:32px}.people .ph{height:220px;margin-bottom:40px}}

/* compare */
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.cmp{width:100%;min-width:860px;border-collapse:collapse;font-size:14px}
table.cmp th,table.cmp td{padding:22px 14px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle;line-height:1.6}
table.cmp thead th{font-size:13px;font-weight:500;color:var(--ink-2);border-bottom:1px solid var(--ink)}
table.cmp tbody th{text-align:left;font-weight:500;white-space:nowrap;background:#fff}
table.cmp .us{background:var(--navy);color:#fff}
table.cmp thead .us{font-weight:700}
table.cmp td small{display:block;font-size:12px;color:var(--mute)}
table.cmp td.us small{color:#a9bcd3}
.mk{display:block;font-size:17px}
.swipe{display:none;font-size:12.5px;color:var(--mute);margin:0 0 10px}
@media (max-width:860px){.swipe{display:block}table.cmp tbody th{position:sticky;left:0;z-index:1}}

/* cases */
.cases{background:var(--mist)}
.case{display:grid;grid-template-columns:5fr 6fr;gap:0;background:#fff;margin-bottom:28px}
.case .ph{min-height:340px}
.case .tx{padding:44px 52px}
.case .no{font-family:var(--en);font-size:13px;letter-spacing:.24em;color:var(--blue);margin:0 0 6px}
.case .tag{font-size:12.5px;color:var(--mute);margin:0 0 10px}
.case h3{font-size:19px;line-height:1.7;margin-bottom:18px}
.case dl{display:flex;flex-wrap:wrap;gap:6px 26px;margin:0 0 18px;font-size:13px;color:var(--ink-2)}
.case dt{display:inline;color:var(--mute);margin-right:8px}
.case dd{display:inline;margin:0}
.case p{margin:0;font-size:14.5px;color:var(--ink-2);padding-top:18px;border-top:1px solid var(--line)}
.cases .note{font-size:12.5px;color:var(--mute)}
@media (max-width:860px){.case{grid-template-columns:1fr}.case .ph{min-height:0;aspect-ratio:16/10}.case .tx{padding:28px 22px 30px}}

/* flow */
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);counter-reset:s;position:relative}
.steps::before{content:"";position:absolute;left:0;right:0;top:22px;height:1px;background:var(--line)}
.steps li{counter-increment:s;padding:0 18px 0 0;position:relative}
.steps li::before{content:counter(s,decimal-leading-zero);position:relative;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--navy);color:#fff;font-family:var(--en);font-size:14px;margin-bottom:22px}
.steps h3{font-size:15.5px;line-height:1.6;margin-bottom:4px}
.steps .t{display:block;font-family:var(--en);font-size:12.5px;color:var(--blue);margin-bottom:10px;letter-spacing:.06em}
.steps p{font-size:13.5px;color:var(--ink-2);margin:0;line-height:1.85}
@media (max-width:1100px){.steps{grid-template-columns:repeat(3,1fr);row-gap:44px}.steps::before{display:none}}
@media (max-width:640px){.steps{grid-template-columns:1fr;row-gap:0}.steps li{display:grid;grid-template-columns:44px 1fr;gap:0 18px;padding:0 0 30px}.steps li::before{grid-row:span 3;margin:0}.steps li::after{content:"";position:absolute;left:21.5px;top:48px;bottom:4px;width:1px;background:var(--line)}.steps li:last-child::after{display:none}}

/* open to all */
.open{margin-top:110px;display:grid;grid-template-columns:5fr 6fr;gap:0;background:var(--navy);color:#fff}
.open .ph{min-height:420px}
.open .tx{padding:56px 60px}
.open h3{font-size:clamp(22px,2.3vw,30px);line-height:1.6;letter-spacing:.06em;margin-bottom:18px}
.open .lead{color:#c4d0de;margin-bottom:26px}
.open ul{list-style:none;margin:0 0 30px;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:0 28px;font-size:14.5px}
.open li{padding:12px 0;border-bottom:1px solid rgba(255,255,255,.18);word-break:keep-all;overflow-wrap:anywhere}
.open .note{font-size:13.5px;color:#c4d0de;margin-bottom:28px}
@media (max-width:1200px){.open ul{grid-template-columns:1fr}}
@media (max-width:960px){.open{grid-template-columns:1fr;margin-top:80px}.open .ph{min-height:0;aspect-ratio:16/9}.open .tx{padding:36px 22px 40px}.open ul{grid-template-columns:1fr}}

/* faq */
.faq .grid{display:grid;grid-template-columns:4fr 8fr;gap:72px}
.faq .sh{grid-template-columns:1fr;margin-bottom:0}
details{border-bottom:1px solid var(--line)}
details:first-of-type{border-top:1px solid var(--ink)}
summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:34px 1fr 20px;gap:12px;padding:26px 0;font-family:var(--fh);font-weight:700;font-size:16px;line-height:1.7}
summary::-webkit-details-marker{display:none}
summary .q{font-family:var(--en);font-weight:400;font-size:20px;color:var(--blue);line-height:1.3}
summary .pm{position:relative;width:14px;height:14px;margin-top:6px}
summary .pm::before,summary .pm::after{content:"";position:absolute;left:0;top:6px;width:14px;height:1px;background:var(--ink);transition:transform .3s}
summary .pm::after{transform:rotate(90deg)}
details[open] summary .pm::after{transform:rotate(0)}
details .a{display:grid;grid-template-columns:34px 1fr;gap:12px;padding:0 32px 26px 0}
details .a span{font-family:var(--en);font-size:20px;color:var(--mute);line-height:1.3}
details .a p{margin:0;color:var(--ink-2);font-size:14.5px}
@media (max-width:900px){.faq .grid{grid-template-columns:1fr;gap:40px}summary{font-size:15px}details .a{padding-right:0}}

/* company */
.company{background:var(--mist)}
.company .grid{display:grid;grid-template-columns:4fr 8fr;gap:72px}
.company .sh{grid-template-columns:1fr;margin-bottom:0}
.company dl{margin:0;border-top:1px solid var(--ink)}
.company dl div{display:grid;grid-template-columns:150px 1fr;gap:16px;padding:20px 0;border-bottom:1px solid var(--line);font-size:15px}
.company dt{color:var(--mute);font-size:13.5px}
.company dd{margin:0}
@media (max-width:900px){.company .grid{grid-template-columns:1fr;gap:40px}.company dl div{grid-template-columns:1fr;gap:2px}}

/* contact */
.contact{padding:0;display:grid;grid-template-columns:5fr 7fr;min-height:100vh}
.contact>.ph{min-height:420px}
.contact .side{position:relative}
.contact .side .cap{position:absolute;left:var(--gut);bottom:48px;right:24px;color:#fff;z-index:2}
.contact .side::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(8,24,46,.75),rgba(8,24,46,0) 55%)}
.contact .side .cap b{display:block;font-family:var(--en);font-weight:300;font-size:56px;line-height:1;margin-bottom:10px}
.contact .body{padding:120px max(48px,env(safe-area-inset-right,0px)) 120px 80px;max-width:820px}
.contact h2{font-size:clamp(22px,2.3vw,30px);line-height:1.7;letter-spacing:.06em;margin-bottom:18px}
.contact .lead{color:var(--ink-2);margin-bottom:40px}
.ways{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--ink);margin-bottom:48px}
.way{padding:22px 18px 20px 0;display:flex;flex-direction:column;gap:6px;border-bottom:1px solid var(--line)}
.way+.way{padding-left:18px;border-left:1px solid var(--line)}
.way b{font-family:var(--fh);font-size:16px;color:var(--navy)}
.way span{font-size:13px;color:var(--ink-2);line-height:1.75;flex:1}
.way i{font-style:normal;font-size:12.5px;color:var(--blue);font-weight:500}
.way:hover b{color:var(--blue)}
.telrow{display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;padding:0 0 32px;margin-bottom:36px;border-bottom:1px solid var(--line)}
.telrow b{font-family:var(--en);font-weight:400;font-size:clamp(32px,3.2vw,44px);color:var(--navy);letter-spacing:.03em;line-height:1}
.telrow span{font-size:13px;color:var(--mute)}
form label{display:block;font-size:13px;font-weight:500;margin:0 0 6px}
form label em{font-style:normal;font-size:11px;color:var(--blue);margin-left:8px}
form input,form select,form textarea{width:100%;border:0;border-bottom:1px solid #b9c4d2;background:transparent;color:var(--ink);font:inherit;font-size:16px;padding:10px 0;margin-bottom:26px;border-radius:0}
form textarea{min-height:110px;resize:vertical}
form input:focus,form select:focus,form textarea:focus{outline:none;border-bottom-color:var(--navy)}
form .r2{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.chk{display:flex;align-items:center;gap:10px;font-size:13px;margin:0 0 28px}
.chk input{width:auto;margin:0}
.sent{border:1px solid var(--navy);padding:28px}
@media (max-width:1200px){.ways{grid-template-columns:1fr}.way+.way{padding-left:0;border-left:0}}
@media (max-width:1000px){.contact{grid-template-columns:1fr;min-height:0}.contact>.ph{min-height:0;height:300px}.contact .body{padding:72px var(--gut) 84px}.contact .side .cap b{font-size:40px}.ways{grid-template-columns:1fr}.way+.way{padding-left:0;border-left:0}form .r2{grid-template-columns:1fr;gap:0}}

/* footer */
footer{background:#081a31;color:#93a3b8;font-size:13px;padding-block:96px 36px}
.fg{display:grid;grid-template-columns:1.6fr 1fr 1fr 1.3fr;gap:48px}
footer .logo b{color:#fff}
footer address{font-style:normal;margin-top:24px;line-height:1.9}
footer h4{font-family:var(--en);color:#fff;font-size:13px;font-weight:500;letter-spacing:.2em;margin:0 0 18px}
footer ul{list-style:none;margin:0;padding:0}
footer li{margin-bottom:10px}
footer a:hover{color:#fff}
.ftel b{display:block;font-family:var(--en);font-size:26px;font-weight:400;color:#fff;letter-spacing:.03em}
.ftel .btn{margin-top:18px;width:100%;min-width:0}
.fb{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;border-top:1px solid #1c3150;margin-top:72px;padding-top:26px;font-size:11.5px}
.pagetop{position:absolute;right:max(48px,env(safe-area-inset-right,0px));top:-28px;width:56px;height:56px;border-radius:50%;background:var(--blue);display:grid;place-items:center;color:#fff}
.pagetop::before{content:"";width:10px;height:10px;border-left:1px solid #fff;border-top:1px solid #fff;transform:rotate(45deg);margin-top:4px}
footer{position:relative}
@media (max-width:900px){.fg{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.fg{grid-template-columns:1fr;gap:36px}.pagetop{right:22px}}

/* floating CTA */
.fcta{position:fixed;right:max(24px,env(safe-area-inset-right,0px));bottom:calc(24px + env(safe-area-inset-bottom,0px));z-index:40;display:flex;align-items:stretch;background:#fff;box-shadow:0 12px 36px rgba(8,24,46,.22);transform:translateY(calc(100% + 48px));transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.fcta.show{transform:none}
.fcta .lab{padding:14px 20px;font-size:12.5px;line-height:1.55;color:var(--ink)}
.fcta .lab b{display:block;font-size:13.5px;color:var(--navy)}
.fcta a.go{display:flex;align-items:center;gap:14px;padding:0 24px;background:var(--blue);color:#fff;font-size:13.5px;font-weight:500}
.fcta a.go:hover{background:var(--navy)}
.fcta .x{position:absolute;right:-10px;top:-10px;width:24px;height:24px;border-radius:50%;background:var(--navy);border:0;color:#fff;font-size:12px;cursor:pointer;line-height:24px}
.mbar{display:none}
@media (max-width:760px){
  .fcta{display:none}
  .mbar{display:grid;grid-template-columns:1fr 1.5fr;position:fixed;left:0;right:0;bottom:0;z-index:40;transform:translateY(110%);transition:transform .35s;padding-bottom:env(safe-area-inset-bottom,0px);background:var(--navy)}
  .mbar.show{transform:none}
  .mbar a{display:flex;align-items:center;justify-content:center;height:58px;font-size:14px;font-weight:500;color:#fff}
  .mbar a+a{background:var(--blue)}
  footer{padding-bottom:110px}
}
.proto{position:fixed;left:12px;bottom:12px;z-index:30;background:rgba(8,24,46,.85);color:#fff;font-size:10.5px;padding:4px 10px}
@media (max-width:760px){.proto{display:none}}


/* ===== design layer ===== */
.flow{background-image:linear-gradient(var(--bg),var(--bg))}
/* offset colour blocks behind photos */
.frame{position:relative}
.frame::before{content:"";position:absolute;inset:28px -28px -28px 28px;background:var(--blue);opacity:.12;z-index:0}
.frame.l::before{inset:28px 28px -28px -28px}
.frame.navy::before{background:var(--navy);opacity:1;inset:-24px 24px 24px -24px}
.frame>.ph{position:relative;z-index:1}
@media (max-width:760px){.frame::before{inset:14px -14px -14px 14px}.frame.l::before{inset:14px 14px -14px -14px}.frame.navy::before{inset:-12px 12px 12px -12px}}
/* vertical Japanese labels */
.vt{position:absolute;top:140px;writing-mode:vertical-rl;font-family:var(--fh);font-weight:500;font-size:13px;letter-spacing:.5em;color:var(--blue);display:flex;align-items:center;gap:14px;z-index:2}
.vt::after{content:"";width:1px;height:80px;background:currentColor;opacity:.5}
.vt.r{right:max(18px,env(safe-area-inset-right,0px))}
.vt.l{left:max(18px,env(safe-area-inset-left,0px))}
.dark .vt,.stance .vt{color:#8fb6ec}
section{position:relative}
@media (max-width:1100px){.vt{display:none}}
/* hero: vertical copy + rotating badge */
.hero .tate{position:absolute;z-index:2;right:max(56px,env(safe-area-inset-right,0px));top:150px;writing-mode:vertical-rl;font-family:var(--fh);font-weight:500;font-size:16px;letter-spacing:.42em;line-height:2.2;opacity:.92}
.badge{position:absolute;z-index:3;right:max(48px,env(safe-area-inset-right,0px));bottom:110px;width:132px;height:132px}
.badge svg{width:100%;height:100%;animation:spin 22s linear infinite}
.badge text{font-family:var(--en);font-size:10.5px;letter-spacing:3.2px;fill:#fff}
.badge i{position:absolute;inset:0;margin:auto;width:46px;height:46px;border-radius:50%;background:var(--blue);display:grid;place-items:center}
.badge i::before{content:"";width:9px;height:9px;border-right:1.5px solid #fff;border-bottom:1.5px solid #fff;transform:rotate(45deg);margin-top:-4px}
@keyframes spin{to{transform:rotate(360deg)}}
@media (max-width:760px){.hero .tate,.badge{display:none}}
/* about: large outlined number-like ornament + blue bar */
.about .catch{position:relative;padding-left:26px}
.about .catch::before{content:"";position:absolute;left:0;top:.5em;bottom:.5em;width:4px;background:linear-gradient(var(--blue),var(--navy))}
/* market: donut charts */
.market .num .donut{flex:none;width:118px;height:118px;border-radius:50%;background:conic-gradient(#5ea2ff calc(var(--v)*1%),rgba(255,255,255,.12) 0);display:grid;place-items:center;position:relative}
.market .num .donut::after{content:"";position:absolute;inset:12px;border-radius:50%;background:var(--navy)}
.market .num .donut span{position:relative;z-index:1;font-family:var(--en);font-size:13px;letter-spacing:.1em;color:#8fb6ec}
.market::before{content:"";position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;border:1px solid rgba(255,255,255,.08);box-shadow:0 0 0 60px rgba(255,255,255,.02),0 0 0 120px rgba(255,255,255,.015)}
@media (max-width:560px){.market .num .donut{width:92px;height:92px}}
/* promise numbers in circles */
.pi .n{width:64px;height:64px;border-radius:50%;border:1px solid var(--blue);display:grid;place-items:center;font-size:24px;background:#fff}
@media (max-width:860px){.pi .n{width:48px;height:48px;font-size:18px}}
/* support rows: number watermark */
.row{position:relative}
.row .tx{position:relative}
.row .tx::before{content:attr(data-no);position:absolute;right:0;top:-78px;font-family:var(--en);font-weight:300;font-size:140px;line-height:1;color:var(--mist);z-index:-1}

@media (max-width:860px){.row .tx::before{font-size:88px;top:-24px}}
/* cta: diagonal accent */
.cta::after{content:"";position:absolute;right:0;top:0;bottom:0;width:38%;background:linear-gradient(115deg,transparent 0 30%,rgba(34,104,200,.55) 30% 100%);z-index:1}
@media (max-width:860px){.cta::after{display:none}}
/* people photo with caption ribbon */
.people .frame{margin-bottom:56px}
.people .frame .ph{margin-bottom:0}
.ribbon{position:absolute;z-index:2;left:0;bottom:0;background:var(--navy);color:#fff;font-family:var(--fh);font-weight:700;font-size:clamp(15px,1.6vw,20px);letter-spacing:.1em;padding:18px 34px}
/* case number big */
.case{position:relative}
.case .no{font-size:15px}
.case .tx::after{content:"";position:absolute;right:0;top:0;width:0;height:0;border-style:solid;border-width:0 54px 54px 0;border-color:transparent var(--blue) transparent transparent}
.case .tx{position:relative}
/* steps: dotted connector */
.steps::before{background:repeating-linear-gradient(90deg,var(--blue) 0 4px,transparent 4px 10px);opacity:.5}
/* section separator wave */
.wave{display:block;width:100%;height:60px;margin-top:-60px;position:relative;z-index:3}

/* reveal (content stays visible without JS) */
.js .rv{opacity:0;transform:translateY(30px);transition:opacity 1s cubic-bezier(.2,.7,.2,1),transform 1s cubic-bezier(.2,.7,.2,1)}
.js .rv.in{opacity:1;transform:none}
.js .mask::after{content:"";position:absolute;inset:0;z-index:2;background:var(--mist);transform-origin:right center;transition:transform 1.2s cubic-bezier(.7,0,.2,1)}
.js .mask.in::after{transform:scaleX(0)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.js .rv{opacity:1;transform:none}.js .mask::after{display:none}}
'''

LOGO='<svg viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 17 L17 9 L26 17" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M11 15 V25 H23 V15" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
AR='<span class="ar"></span>'

hero_slides=[('Q6sCJFHCubc','東京の住宅街',False),('-MVSfkR4xz4','緑に囲まれた東京の住宅',True),('TJ4CndIc9z8','山梨の住宅街',True),('pcYN7Pi8_BQ','夕暮れの東京の住宅街',True)]
slides=''.join(f'<div class="slide ph{" on" if i==0 else ""}">{img(pid,alt,2400,lazy)}</div>' for i,(pid,alt,lazy) in enumerate(hero_slides))

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'viz.py')).read())
SUPPORT_MORE={'MARKETING':['反響数・来場数・成約率を、グループ共通の管理表で毎月集計','Google広告・Meta広告の運用と、媒体ごとの反響単価の比較','ホームページのSEO対策と、Googleマップ（MEO）の口コミ・情報の整備','完成見学会の集客設計と、施主様からの紹介が生まれる仕組みづくり'],
 'RECRUITING':['グループ合同の会社説明会と、新卒・中途の求人','求人媒体・人材紹介会社とのグループ一括契約','入社時研修と、設計・現場監督・大工の職種別の育成','評価制度・給与テーブルの整備（各社の実情に合わせて）'],
 'FINANCE':['月次決算と、翌月10日までの数字の共有','13週の資金繰り表で、資金不足を事前に防ぐ','金融機関との借入条件の交渉と、社長の個人保証の解除','モデルハウス・分譲用地など、大きな投資の判断を一緒に行う'],
 'OPERATIONS':['住設・建材・構造材の共同購買と、仕入れ値の見直し','見積・実行予算・工程・顧客管理のシステム統一','定期点検の履歴をデータ化し、アフターの抜け漏れを防ぐ','省エネ基準の義務化など、法改正への対応をグループで準備']}
support=[
 ('集客','MARKETING','q1tyQip5AQQ','大阪の住宅の外観','広告費あたりの反響数を毎月計測し、媒体と予算の配分を見直します。勘と経験に頼っていた集客を、数字で回る仕組みに置き換えます。','Google・Meta広告の運用、SEO・Googleマップ対策、反響の集計','見学会の企画、施主様からの紹介づくり'),
 ('採用','RECRUITING','4UVtFIfK1eo','建築中の住宅','一社では出せない規模の求人を、グループとして出します。設計・現場監督・大工の採用と、入社後の研修までを引き受けます。','新卒・中途の合同採用、求人媒体の一括契約、入社時研修','配属後の育成、現場での指導'),
 ('財務・資金','FINANCE','4mEyvORkbN0','契約の握手','月次決算と予実管理で、利益が手元に残る構造をつくります。金融機関との交渉や、モデルハウス・用地への投資判断も一緒に行います。','月次決算、資金繰り表、金融機関との交渉','個別案件の見積と受注判断'),
 ('仕入・業務','OPERATIONS','4UVtFIfK1eo','足場のかかった建物','グループの発注量をまとめて建材・設備の原価を下げ、見積・工程・顧客管理を仕組みにして事務作業の時間を減らします。','共同購買、管理システムの統一、点検履歴のデータ化','仕様・設計の判断、施主様との打ち合わせ、現場での判断'),
]
rows=''.join(f'''<article class="row"><div class="frame{' l' if k%2 else ''}"><div class="ph mask viz">{VIZ[en]}</div></div><div class="tx rv" data-no="0{k+1}"><p class="n">{en}</p><h3>{ja}</h3>{P(desc)}<ul class="rw-l">{''.join(f'<li>{x}</li>' for x in SUPPORT_MORE[en])}</ul><dl><div><dt>グループが担う</dt><dd>{nb(g,8)}</dd></div><div><dt>各社に残す</dt><dd>{nb(kk,8)}</dd></div></dl></div></article>''' for k,(ja,en,pid,alt,desc,g,kk) in enumerate(support))

promises=[('社名・|屋号は|そのまま|残します','看板も、ホームページも、職人さんの作業着も変えません。地域で積み上げた名前が、いちばんの資産です。'),
 ('雇用と|給与水準を|守ります','グループ入りを理由にした人員削減や給与の引き下げは行いません。期間は契約書に明記します。'),
 ('保証と|定期点検を|引き継ぎます','引き渡し済みの家の保証・点検・アフター対応は、原則として、これまでの担当者が続けます。'),
 ('取引先とは、|適正な|条件で|向き合います','長年の協力業者さんとの関係は大切にします。そのうえで仕入れ値・外注費は相場と照らして見直し、品質・納期・価格の3つを基準に、適正な条件で交渉します。'),
 ('社長の|個人保証の|解除に|取り組みます','借入に付いている社長個人の保証は、金融機関と協議のうえ、クロージング時点での解除を目指します。')]
plist=''.join(f'<div class="pi rv"><span class="n">{i+1:02d}</span><h3>{W(h)}</h3>{P(t)}</div>' for i,(h,t) in enumerate(promises))

people=[('社長へ','辞める|時期は、|ご自身で|決められます。','引き継ぎ期間だけ残る形も、社長を続ける形も選べます。個人保証の解除と後継者の育成も、一緒に進めます。'),
 ('社員の皆さまへ','現場の|仕事と|職場は|変わりません。','職場も上司も名刺の社名もそのままです。事務作業が減り、研修とキャリアの選択肢が増えます。'),
 ('施主様へ','保証も|点検も、|これまで|どおりです。','保証も定期点検も窓口も変わりません。施工中の工事も、契約どおりにお引き渡しします。'),
 ('協力業者さんへ','いい仕事には、|適正な|価格で|応えます。','品質・納期・価格を基準にお取引します。グループの他社の現場をお願いする機会も増えていきます。')]
pg=''.join(f'<article class="rv"><p class="who">{w}</p><h3>{W(h)}</h3>{P(t)}</article>' for w,h,t in people)

cases=[('後継者不在','TJ4CndIc9z8','沖縄の住宅','子どもは|別の道へ。|社員に|継がせるには|資金が|足りない。','地方都市','年商 約8億円・年間引き渡し25棟','68歳・創業者','株式を引き受け、社長は2年間会長として残留。番頭格の社員を次期社長として育成し、個人保証はクロージング時に解除しました。'),
 ('成長の壁','4UVtFIfK1eo','木造の骨組み','受注は|あるのに、|人が|採れず|年20棟から|伸びない。','首都圏郊外','年商 約6億円・年間引き渡し20棟','55歳・二代目','社長は続投。グループの合同採用で設計・現場監督を確保し、集客と管理部門をグループに移して、社長が営業と現場に集中できるようにしました。'),
 ('廃業の検討','q1tyQip5AQQ','大きな窓のある室内','体力的に|限界。|でも|施主様の|アフターだけは|残したい。','地方の郡部','年商 約3億円・リフォーム中心','72歳・創業者','近隣のグループ会社と管理部門を共通化。社名とアフター窓口を残したまま、社長は半年で引退しました。')]
cs=''.join(f'''<article class="case"><div class="ph mask">{img(pid,alt,1200)}</div><div class="tx rv"><p class="no">CASE {i+1:02d}</p><p class="tag">{tag}</p><h3>{W(h)}</h3><dl><div><dt>エリア</dt><dd>{a}</dd></div><div><dt>規模</dt><dd>{sz}</dd></div><div><dt>社長</dt><dd>{ceo}</dd></div></dl>{P(t)}</div></article>''' for i,(tag,pid,alt,h,a,sz,ceo,t) in enumerate(cases))

steps=[('初回面談','1〜2時間','会社とご家族、ご自身の今後について伺います。決算書は不要です。'),('秘密保持契約・|資料のご提供','2〜4週間','決算書・受注残・社員構成などを拝見します。'),('条件の|ご提示','2〜3週間','譲渡価格の考え方、雇用、引き継ぎ期間を書面でお示しします。'),('詳細調査','1〜2ヶ月','財務・法務・労務、施工中物件、保証履歴、建設業許可を確認します。'),('最終契約・|お支払い','約1ヶ月','株式譲渡契約を結び、個人保証の解除に向けて金融機関と協議します。'),('ご説明と|引き継ぎ','6ヶ月〜','社員・施主様への説明に、私たちも同席します。')]
st=''.join(f'<li class="rv"><h3>{W(h)}</h3><span class="t">{t}</span>{P(p)}</li>' for h,t,p in steps)

faqs=[('相談したことが、社員や取引先に知られることはありませんか。','ご了承なくお伝えすることはありません。面談は社外かオンラインで行い、郵送物や電話も事前に決めた方法でのみご連絡します。秘密保持契約はご希望があれば初回面談の前に結べます。'),
 ('社員には、いつ、どう伝えればいいですか。','原則として最終契約の後です。幹部に先に伝えるか、全員に一度に伝えるかは会社によって違うため、順番と話す内容を一緒に準備します。説明の場には私たちも同席します。'),
 ('譲渡価格はどのように決まりますか。','純資産に、今後数年分の利益を踏まえた収益力を加えて算定するのが基本です。受注残や保有不動産、退職金の支給なども考慮し、計算の根拠は書面でお示しします。'),
 ('赤字の会社でも相談できますか。','はい。赤字の理由と、改善の見通しを一緒に整理するところから始めます。グループ入りが最善でない場合は、その理由と別の選択肢をお伝えします。'),
 ('建設業許可はそのまま使えますか。','株式譲渡であれば会社そのものは変わらないため、許可は引き継がれます。常勤役員等（いわゆる経管）や営業所技術者が退任される場合は後任が必要になるため、交代の時期を事前に設計します。'),
 ('社長は辞めなければいけませんか。','いいえ。引き継ぎ期間だけ残る形も、社長を続ける形もあります。ご本人の希望と、次の社長候補の状況をふまえて決めます。'),
 ('数年後に、別の会社へ売られることはありませんか。','買った会社を売却して利益を得ることを前提にしていません。グループ会社が毎年生む利益で、長く経営を続ける考え方です。')]
fq=''.join(f'<details><summary><span class="q">Q.</span><span>{nb(q,6)}</span><span class="pm"></span></summary><div class="a"><span>A.</span>{P(a)}</div></details>' for q,a in faqs)

HTML=f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>株式会社エッジアセット｜工務店・住宅会社の事業承継</title>
<meta name="description" content="株式会社エッジアセットは、後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営する事業承継の受け皿です。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Noto+Sans+JP:wght@400;500;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>

</head>
<body>

<header class="site">
  <div class="w">
    <a class="logo" href="#top">{LOGO}<span><b>EDGE ASSET</b><small>株式会社エッジアセット</small></span></a>
    <nav class="gnav" aria-label="メインメニュー">
      <a class="nl" href="#about">私たちについて</a>
      <a class="nl" href="#promise">お約束</a>
      <a class="nl" href="#support">グループの支援</a>
      <a class="nl" href="#cases">事例</a>
      <a class="nl" href="#flow">ご相談の流れ</a>
      <a class="nl" href="#faq">よくある質問</a>
      <span class="tel">03-0000-0000<small>平日 9:00–18:00</small></span>
      <a class="btn btn-white" href="#contact">無料相談 {AR}</a>
    </nav>
  </div>
</header>

<main id="top">

<section class="hero" aria-label="メインビジュアル">
  {slides}
  <div class="copy"><div class="w">
    <p class="en">BUSINESS SUCCESSION FOR HOME BUILDERS</p>
    <h1>{W('建てた|家の|点検に、|三十年後も|伺える|会社で|あるために。')}</h1>
    {P('エッジアセットは、後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営する事業承継の受け皿です。社名・社員・施主様へのアフターのお約束を、そのまま引き継ぎます。','lead')}
    <div class="btns"><a class="btn btn-white" href="#contact">無料で相談する {AR}</a><a class="btn btn-ghost" href="#flow">ご相談の流れを見る {AR}</a></div>
  </div></div>
  <a class="badge" href="#about" aria-label="下へスクロール"><svg viewBox="0 0 132 132" aria-hidden="true"><defs><path id="c" d="M66,66 m-52,0 a52,52 0 1,1 104,0 a52,52 0 1,1 -104,0"/></defs><text><textPath href="#c">SCROLL DOWN · EDGE ASSET · SINCE 2026 · </textPath></text></svg><i></i></a>
  <div class="news"><div class="w">
    <b>NEWS</b><time datetime="2026-10-22">2026.10.22</time><span class="t">コーポレートサイトを公開しました。</span>
    <div class="pager" id="pager"><span id="cnt">01</span></div>
  </div></div>
</section>

<section class="about" id="about">
  <span class="bgword" aria-hidden="true">Succession</span>
  <div class="w grid">
    <div class="rv">
      {head('About','私たちについて','') .replace('<h2></h2>','')}
      <p class="catch">{W('家は、|建てた後の|三十年の|ほうが長い。')}</p>
      <div class="body">
        {P('工務店の社長から事業承継の相談を受けると、最初に出てくるのはご自身のことではなく、社員と、これまで家を建てさせてもらった施主様のことです。「自分が辞めたら、あの家の点検には誰が行くのか」。')}
        {P('エッジアセットは、その問いに答えるための会社です。株式を引き受けたあとも社名と現場はそのままに、集客・採用・財務・管理部門といった、一社では手が回らない仕事をグループで支えます。')}
      </div>
      <a class="tl" href="#support">グループの支援を見る {AR}</a>
    </div>
    <div class="pics">
      <div class="ph p1 mask">{img('4UVtFIfK1eo','木造の骨組み',1600,fb=['4UVtFIfK1eo'])}</div>
      <div class="ph p2 mask">{img('q1tyQip5AQQ','大きな窓のある室内',900,fb=['q1tyQip5AQQ'])}</div>
    </div>
  </div>
</section>

<section class="market dark" id="market">
  <div class="w grid">
    <div class="rv">
      {head('Market','業界の現状','後継者が|いない|会社が|いちばん|多い|業種は、|建設業です。')}
      <div class="num"><span class="donut" style="--v:57.3"><span>建設業</span></span><strong>57.3<small>%</small></strong><div><h3>{W('建設業の|後継者不在率')}</h3>{P('業種別で最も高い水準。全国平均を7ポイント上回ります。')}</div></div>
      <div class="num"><span class="donut" style="--v:50.1"><span>全国</span></span><strong>50.1<small>%</small></strong><div><h3>{W('全国企業の|後継者不在率')}</h3>{P('いまも2社に1社は、後継者が決まっていません。')}</div></div>
      <p class="src">出典：帝国データバンク「全国企業『後継者不在率』動向調査（2025年）」</p>
    </div>
    <div class="frame l"><div class="ph mask">{img('pcYN7Pi8_BQ','夜の東京の住宅街',1200)}</div></div>
  </div>
</section>

<div class="strip" aria-hidden="true">
  <div class="ph">{img('4mEyvORkbN0','',1200)}</div>
  <div class="ph">{img('q1tyQip5AQQ','',800)}</div>
  <div class="ph">{img('rD28m9BmXVs','',1000)}</div>
  <div class="ph">{img('-MVSfkR4xz4','',800)}</div>
</div>

<section class="stance">
  <div class="ph">{img('rD28m9BmXVs','',2000)}</div>
  <div class="w">
    <p class="big rv">売らない。</p>
    <div class="rv">
      {P('私たちは、買った会社を数年で売却して利益を得るファンドではありません。グループに入っていただいた会社は、原則として手放さずに経営を続けます。')}
      {P('売却益ではなく、毎年の営業利益で成り立つグループです。だからこそ、利益がきちんと残る経営に本気で取り組みます。')}
      {P('目指すのは、社員の給与が上がり、施主様からの紹介が続く会社であることです。')}
    </div>
  </div>
</section>

<section class="msg" id="message">
  <div class="w grid">
    <div class="rv">
      <div class="frame navy"><div class="ph">{img('rD28m9BmXVs','大阪のオフィスビル',1000)}<span>代表写真は撮影予定</span></div></div>
      <div class="who"><small>代表取締役</small><b>谷岡 佑亮</b></div>
      <ul class="career"><li>株式会社船井総合研究所にて、上位0.5%の年間粗利獲得実績を複数年にわたり達成</li><li>経営再建・成長戦略の実行支援を中心に、実務型のコンサルティングに従事</li><li>同社を退職後、複数の事業運営に携わりながら、建築業界をはじめとする企業の人材採用・営業体制の構築・業務改善を支援</li><li>株式会社エッジアセット 代表取締役</li></ul>
    </div>
    <div class="letter rv">
      {head('Message','代表メッセージ','').replace('<h2></h2>','')}
      <p class="lede">{W('会社を|売る、|という|言葉に|抵抗がある方へ。')}</p>
      {P('経営コンサルタントとして、そして事業の運営者として、建築業界を中心に、さまざまな会社の経営の支援に携わってきました。黒字で、腕のいい職人がいて、地域で信頼されている。それでも、継ぐ人がいないという一点で、会社をたたむ選択を考える社長に、何度も出会ってきました。')}
      {P('大手に売れば、名前は数年で消えるかもしれない。ファンドに売れば、数年後にまた別の誰かに売られるかもしれない。その不安があるから、多くの社長は相談すること自体をためらいます。')}
      {P('私たちは、その不安に正面から答えるために会社をつくりました。名前を残すこと、施主様との約束を守ること。どちらも契約書に書き込みます。売却を前提にしないことも、最初にはっきりお伝えします。まずは一度、話を聞かせてください。')}
      <p class="sign"><span class="nb">株式会社エッジアセット</span>　<span class="nb">代表取締役　谷岡 佑亮</span></p>
    </div>
  </div>
</section>

<section class="promise" id="promise">
  <div class="w">
    {head('Promise','5つのお約束','引き継ぐ|ときに、|契約書で|お約束すること','口約束ではなく、株式譲渡契約の条項として書き込みます。そのかわり、私たちからお願いすることも正直にお伝えします。')}
    <div class="plist">
      {plist}
      <div class="pi ask rv"><h3>そのかわり、お願いすること</h3><ul><li>月次の数字は、毎月一緒に確認させてください。</li><li>経理・労務・情報管理は、グループ共通のルールに合わせていただきます。</li><li>仕入れ・外注の条件は、グループの基準で一緒に見直させてください。</li><li>譲渡価格は純資産と収益力から算定します。相場を大きく超える金額はお出しできません。</li></ul></div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="ph">{img('pcYN7Pi8_BQ','',2000)}</div>
  <div class="w">
    <div class="rv"><h2>{W('まずは|30分、|オンラインで|話を|聞いて|みませんか。')}</h2>{P('ご相談は無料です。社名を伏せたままでも構いません。')}<p class="tel">お電話でのご相談<b>03-0000-0000</b></p></div>
    <div class="btns rv"><a class="btn btn-white" href="#contact">面談を予約する {AR}</a><a class="btn btn-ghost" href="#faq">よくある質問を見る {AR}</a></div>
  </div>
</section>

<section class="support" id="support">
  <div class="w">
    {head('Support','グループの支援','現場は|変えずに、|一社では|手が回らない|仕事を|支えます','家づくりの方針には口を出しません。規模が小さいほど負担が重くなる仕事を、グループでまとめて引き受けます。')}
    {rows}
  </div>
</section>

<section class="people">
  <div class="w">
    {head('People','それぞれの方へ','社長・|社員・|施主様・|協力業者さん、|それぞれへの|お約束')}
    <div class="frame"><div class="ph mask">{img('-MVSfkR4xz4','緑に囲まれた住宅',2000)}</div><p class="ribbon">{W("社名も、|社員も、|施主様との|約束も。".replace("約束も。","約束も。"))}</p></div>
    <div class="pg">{pg}</div>
  </div>
</section>

<section class="compare" id="compare">
  <div class="w">
    {head('Comparison','他の選択肢との比較','事業承継の|選択肢を|比べて|みてください','どの方法にも長所と短所があります。私たちが合わない場合は、ほかの選択肢をご案内することもあります。')}
    <p class="swipe">表は横にスクロールできます</p>
    <div class="tbl rv">
      <table class="cmp">
        <thead><tr><th></th><th>親族・社員への承継</th><th>大手・同業への売却</th><th>一般的な投資ファンド</th><th class="us">エッジアセット</th><th>廃業</th></tr></thead>
        <tbody>
          <tr><th>社名・屋号</th><td><span class="mk">◎</span>残る</td><td><span class="mk">△</span>統合されることが多い</td><td><span class="mk">○</span>残ることが多い</td><td class="us"><span class="mk">◎</span>契約で残す</td><td><span class="mk">×</span>なくなる</td></tr>
          <tr><th>社員の雇用</th><td><span class="mk">◎</span></td><td><span class="mk">△</span><small>重複部門は再編</small></td><td><span class="mk">○</span></td><td class="us"><span class="mk">◎</span><small>期間を定めて契約で約束</small></td><td><span class="mk">×</span></td></tr>
          <tr><th>施主様の保証・点検</th><td><span class="mk">◎</span></td><td><span class="mk">○</span></td><td><span class="mk">○</span></td><td class="us"><span class="mk">◎</span><small>原則として担当者が継続</small></td><td><span class="mk">×</span><small>引き受け手がいない</small></td></tr>
          <tr><th>社長の個人保証</th><td><span class="mk">△</span><small>後継者に移る</small></td><td><span class="mk">◎</span></td><td><span class="mk">◎</span></td><td class="us"><span class="mk">◎</span><small>解除に取り組む</small></td><td><span class="mk">△</span><small>清算次第</small></td></tr>
          <tr><th>数年後の再売却</th><td>なし</td><td>なし</td><td><span class="mk">×</span><small>3〜7年で売却が前提</small></td><td class="us"><span class="mk">◎</span><small>前提にしない</small></td><td>なし</td></tr>
          <tr><th>住宅業界の実務支援</th><td><span class="mk">△</span></td><td><span class="mk">○</span></td><td><span class="mk">△</span><small>業界によって異なる</small></td><td class="us"><span class="mk">◎</span><small>集客・採用・財務を本部が担う</small></td><td>なし</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:12.5px;color:var(--mute);margin-top:16px">一般的な傾向を整理したもので、個別の案件により異なります。</p>
  </div>
</section>

<section class="cases" id="cases">
  <div class="w">
    {head('Case','モデルケース','こんな|ご相談を|お受け|しています','よくあるご相談を、条件を変えた想定事例としてまとめました。実在の企業ではありません。')}
    {cs}
    <div class="btns" style="margin-top:44px"><a class="btn btn-navy" href="#contact">似た状況について相談する {AR}</a></div>
  </div>
</section>

<section class="flow" id="flow">
  <div class="w">
    {head('Flow','ご相談の流れ','ご相談から|最終契約まで、|通常は|半年前後です','ご了承なく、社員や取引先にお伝えすることはありません。面談は社外かオンラインで行います。')}
    <ol class="steps">{st}</ol>
    <div class="open">
      <div class="ph">{img('Q6sCJFHCubc','東京の住宅街',1400)}</div>
      <div class="tx rv">
        <h3>{W('規模や|エリアだけで、|お断りする|ことは|ありません。')}</h3>
        {P('年商や棟数、赤字か黒字かで門前払いすることはありません。リフォーム専業、設計事務所、不動産と兼業の会社も含めて、住まいに関わる会社であればまずはお話を伺います。','lead')}
        <ul>{''.join('<li>'+W(x)+'</li>' for x in ['後継者が|決まっていない','数年以内に|引退を|考えている','赤字が続いて|先行きが|不安','人が採れず、|成長が|止まっている','廃業も|選択肢に|入れている','社員と|施主様の|今後が心配'])}</ul>
        <p class="note">{W('ひとつでも|当てはまれば、|ご相談ください。|決算書は|なくても|構いません。')}</p>
        <a class="btn btn-white" href="#contact">まずは話を聞いてみる {AR}</a>
      </div>
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="w grid">
    <div class="rv">{head('FAQ','よくあるご質問','ご相談の|前に|よく|聞かれること')}</div>
    <div class="rv">{fq}</div>
  </div>
</section>

<section class="company" id="company">
  <div class="w grid">
    <div class="rv">{head('Company','会社概要','会社概要')}</div>
    <dl class="rv">
      <div><dt>社名</dt><dd>株式会社エッジアセット（EDGE ASSET Inc.）</dd></div>
      <div><dt>代表者</dt><dd>代表取締役　谷岡 佑亮</dd></div>
      <div><dt>所在地</dt><dd>〒105-0022　東京都港区海岸2丁目5-1-1702</dd></div>
      <div><dt>設立</dt><dd><em class="tbd">【確定後に記載】</em></dd></div>
      <div><dt>資本金</dt><dd><em class="tbd">【確定後に記載】</em></dd></div>
      <div><dt>事業内容</dt><dd>工務店・住宅会社の株式取得および経営／<span class="nb">グループ会社の経営支援</span></dd></div>
      <div><dt>連絡先</dt><dd>TEL 03-0000-0000（平日 9:00–18:00）</dd></div>
    </dl>
  </div>
</section>

<section class="contact" id="contact">
  <div class="ph side">{img('Q6sCJFHCubc','家の鍵を持つ手',1400,fb=['-MVSfkR4xz4'])}<p class="cap"><b>Contact</b>お問い合わせ</p></div>
  <div class="body">
    <h2>{W('まずは、|話を|聞いてみる|だけで|構いません')}</h2>
    {P('ご相談は無料です。お名前を伏せたままのご相談もお受けします。いただいた内容を、ご本人の同意なく第三者に伝えることはありません。','lead')}
    <div class="ways">
      <a class="way" href="#cf" data-topic="面談の予約"><b>面談を予約する</b><span>代表が直接お会いします。<span class="nb">社外でもオンラインでも</span><span class="nb">構いません。</span></span><i>日程を相談する</i></a>
      <a class="way" href="#cf" data-topic="電話での相談"><b>電話で相談する</b><span>平日9時〜18時。<span class="nb">夜間・土日も調整します。</span></span><i>03-0000-0000</i></a>
      <a class="way" href="#cf" data-topic="匿名での相談"><b>匿名で相談する</b><span>社名を出さずに、状況だけお聞かせください。</span><i>匿名で送る</i></a>
    </div>
    <div class="telrow"><b>03-0000-0000</b><span>平日 9:00–18:00　夜間・土日の面談も調整します</span></div>
    <form id="cf" novalidate>
      <label for="f-topic">ご相談の種類</label>
      <select id="f-topic"><option>面談の予約</option><option>電話での相談（折り返し希望）</option><option>匿名での相談</option><option>その他</option></select>
      <div class="r2"><div><label for="f-name">お名前</label><input id="f-name" autocomplete="name"></div><div><label for="f-co">会社名</label><input id="f-co" autocomplete="organization"></div></div>
      <div class="r2"><div><label for="f-mail">メールアドレス<em>必須</em></label><input id="f-mail" type="email" autocomplete="email" required></div><div><label for="f-tel">電話番号</label><input id="f-tel" type="tel" autocomplete="tel"></div></div>
      <label for="f-msg">ご相談内容</label><textarea id="f-msg"></textarea>
      <label class="chk"><input type="checkbox" id="f-ok"> プライバシーポリシーに同意する</label>
      <button class="btn btn-navy" type="submit">送信する {AR}</button>
    </form>
    <div class="sent" id="sent" hidden><p style="font-size:17px;margin-bottom:6px">送信を受け付けました。</p><p style="margin:0;font-size:13px;color:var(--mute)">2営業日以内にご連絡します。（デモのため実際には送信されません）</p></div>
  </div>
</section>

</main>

<footer>
  <a class="pagetop" href="#top" aria-label="ページの先頭へ"></a>
  <div class="w">
    <div class="fg">
      <div><a class="logo" href="#top" style="color:#fff"><span><b>EDGE ASSET</b><small>株式会社エッジアセット</small></span></a><address>〒105-0022<br>東京都港区海岸2丁目5-1-1702</address></div>
      <div><h4>COMPANY</h4><ul><li><a href="#about">私たちについて</a></li><li><a href="#message">代表メッセージ</a></li><li><a href="#compare">他の選択肢との比較</a></li><li><a href="#company">会社概要</a></li></ul></div>
      <div><h4>SUCCESSION</h4><ul><li><a href="#promise">5つのお約束</a></li><li><a href="#support">グループの支援</a></li><li><a href="#cases">モデルケース</a></li><li><a href="#flow">ご相談の流れ</a></li><li><a href="#faq">よくあるご質問</a></li></ul></div>
      <div class="ftel"><h4>CONTACT</h4><b>03-0000-0000</b><span>平日 9:00–18:00</span><a class="btn btn-blue" href="#contact">無料で相談する {AR}</a></div>
    </div>
    <div class="fb"><span><a href="#top">プライバシーポリシー</a>　｜　<a href="#top">サイトのご利用について</a></span><span>© EDGE ASSET Inc.</span></div>
    <p style="font-size:10.5px;color:#5f7290;margin-top:10px">写真：Unsplash（仮素材）</p>
  </div>
</footer>

<aside class="fcta" id="fcta" aria-label="ご相談窓口">
  <div class="lab"><b>秘密厳守・無料のご相談</b>社名を伏せたままでも構いません</div>
  <a class="go" href="#contact">相談する {AR}</a>
  <button class="x" id="fx" aria-label="閉じる">×</button>
</aside>
<nav class="mbar" id="mbar" aria-label="ご相談"><a href="#contact">電話で相談</a><a href="#contact">無料で相談する</a></nav>
<div class="proto">デザイン確認用｜文言・数値・写真は仮</div>

<script>
(() => {{
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const slides = $$('.slide'), pager = $('#pager'), cnt = $('#cnt');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cur = 0, timer;
  slides.forEach((_, i) => {{
    const b = document.createElement('button');
    b.setAttribute('aria-label', '写真 ' + (i + 1));
    b.addEventListener('click', () => go(i));
    pager.appendChild(b);
  }});
  const bars = $$('button', pager);
  const go = i => {{
    slides[cur].classList.remove('on'); bars[cur].classList.remove('on');
    cur = i; slides[cur].classList.add('on');
    void bars[cur].offsetWidth; bars[cur].classList.add('on');
    cnt.textContent = String(cur + 1).padStart(2, '0');
    clearTimeout(timer);
    if (!still) timer = setTimeout(() => go((cur + 1) % slides.length), 6000);
  }};
  go(0);

  const io = new IntersectionObserver(es => es.forEach(e => {{
    if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
  }}), {{ threshold: .12, rootMargin: '0px 0px -40px 0px' }});
  $$('.rv, .mask').forEach(el => io.observe(el));
  if (!('IntersectionObserver' in window)) $$('.rv, .mask').forEach(el => el.classList.add('in'));

  const hero = $('.hero'), contact = $('#contact'), fcta = $('#fcta'), mbar = $('#mbar');
  let closed = false;
  const onScroll = () => {{
    const past = scrollY > hero.offsetHeight * .8;
    const r = contact.getBoundingClientRect();
    const near = r.top < innerHeight && r.bottom > 0;
    fcta.classList.toggle('show', past && !near && !closed);
    mbar.classList.toggle('show', past && !near);
  }};
  addEventListener('scroll', onScroll, {{ passive: true }}); onScroll();
  $('#fx').addEventListener('click', () => {{ closed = true; onScroll(); }});

  $$('.way').forEach(a => a.addEventListener('click', () => {{ $('#f-topic').value = a.dataset.topic; }}));
  $('#cf').addEventListener('submit', e => {{
    e.preventDefault();
    const mail = $('#f-mail');
    if (!mail.value || !mail.checkValidity()) {{ mail.focus(); mail.style.borderBottomColor = '#c0392b'; return; }}
    e.target.hidden = true; $('#sent').hidden = false;
  }});
}})();
</script>
</body>
</html>
'''

# ====================== multi-page assembly ======================
import re, os
OUT=os.path.dirname(os.path.abspath(sys.argv[1]))
def cut(pattern):
    m=re.search(pattern,HTML,re.S); assert m, pattern; return m.group(0)
css_main=cut(r'(?<=<style>).*?(?=</style>)')
js_main=cut(r'(?<=<script>\n).*?(?=</script>\n</body>)')
head_links=cut(r'<link rel="preconnect".*?display=swap" rel="stylesheet">')
sec={}
for key,pat in {
 'market':r'<section class="market dark" id="market">.*?</section>',
 'about':r'<section class="about" id="about">.*?</section>',
 'stance':r'<section class="stance">.*?</section>',
 'msg':r'<section class="msg" id="message">.*?</section>',
 'promise':r'<section class="promise" id="promise">.*?</section>',
 'cta':r'<section class="cta">.*?</section>',
 'support':r'<section class="support" id="support">.*?</section>',
 'people':r'<section class="people">.*?</section>',
 'compare':r'<section class="compare" id="compare">.*?</section>',
 'cases':r'<section class="cases" id="cases">.*?</section>',
 'flow':r'<section class="flow" id="flow">.*?</section>',
 'faq':r'<section class="faq" id="faq">.*?</section>',
 'company':r'<section class="company" id="company">.*?</section>',
 'contact':r'<section class="contact" id="contact">.*?</section>',
 'footer':r'<footer>.*?</footer>',
}.items(): sec[key]=cut(pat)

JSONLD='<script type="application/ld+json">'+__import__('json').dumps({"@context":"https://schema.org","@type":"Organization","name":"株式会社エッジアセット","alternateName":"EDGE ASSET Inc.","description":"工務店・住宅会社の事業承継（株式取得およびグループ経営）","address":{"@type":"PostalAddress","postalCode":"105-0022","addressRegion":"東京都","addressLocality":"港区","streetAddress":"海岸2丁目5-1-1702","addressCountry":"JP"},"telephone":"03-0000-0000","founder":{"@type":"Person","name":"谷岡佑亮"}},ensure_ascii=False)+'</script>'
PAGES=[('index.html','トップ'),('service.html','グループの支援'),('company.html','私たちについて'),('partners.html','仲介会社・金融機関の皆さまへ'),('news.html','お知らせ'),('contact.html','ご相談・お問い合わせ')]
def nav():
    items=[('company.html','私たちについて'),('service.html','グループの支援'),('cases.html','事例'),('flow.html','ご相談の流れ'),('partners.html','仲介会社・金融機関の方へ'),('news.html','お知らせ')]
    NT=' target="_blank" rel="noopener"'
    links=''.join(f'<a class="nl" href="{h}"{NT}>{t}</a>' for h,t in items)
    menu=[('index.html','トップ','Top'),('company.html','私たちについて','About us'),('service.html','グループの支援','Our support'),('cases.html','事例','Case'),('flow.html','ご相談の流れ','Flow'),('partners.html','仲介会社・金融機関の皆さまへ','For partners'),('news.html','お知らせ','News'),('column.html','コラム','Column'),('contact.html','ご相談・お問い合わせ','Contact')]
    mlinks=''.join(f'<li><a href="{h}"{NT}><span class="mn">{i+1:02d}</span><span class="mt"><span class="me">{e}</span><span class="mj">{j}</span></span><span class="mx" aria-hidden="true"></span></a></li>' for i,(h,j,e) in enumerate(menu))
    return f"""<header class="site">
  <div class="w">
    <a class="logo" href="index.html"><span><b>EDGE ASSET</b><small>株式会社エッジアセット</small></span></a>
    <nav class="gnav" aria-label="メインメニュー">{links}
      <span class="tel">03-0000-0000<small>平日 9:00–18:00</small></span>
      <a class="btn btn-navy" href="contact.html"{NT}>ご相談 {AR}</a>
    </nav>
  </div>
</header>
<button class="burger" id="burger" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="menu"><span class="bl"><i></i><i></i></span><em class="b-o">MENU</em><em class="b-c">CLOSE</em></button>
<div class="menu" id="menu" aria-hidden="true">
  <div class="menu-in">
    <div class="menu-l">
      <p class="menu-t">MENU</p>
      <ul class="menu-list">{mlinks}</ul>
    </div>
    <div class="menu-r">
      <p class="menu-k">ご相談窓口</p>
      <p class="menu-tel">03-0000-0000</p>
      <p class="menu-s">平日 9:00–18:00　夜間・土日の面談も調整します</p>
      <a class="btn btn-white" href="contact.html"{NT}>無料で相談する {AR}</a>
      <p class="menu-addr">株式会社エッジアセット<br>〒105-0022 東京都港区海岸2丁目5-1-1702</p>
      <p class="menu-note">各ページは新しいタブで開きます</p>
    </div>
  </div>
</div>"""
def phero(en,ja,lead,pid):
    return f"""<section class="phero">
  <div class="ph">{img(pid,'',2000,False)}</div>
  <div class="w"><p class="crumb"><a href="index.html">トップ</a><span>/</span>{ja}</p><p class="pen">{en}</p><h1>{W(ja)}</h1>{P(lead,'plead') if lead else ''}</div>
</section>"""
def footer():
    f=sec['footer']
    f=f.replace('href="#top"','href="index.html"').replace('href="#about"','href="company.html"').replace('href="#message"','href="company.html#message"').replace('href="#compare"','href="company.html#compare"').replace('href="#company"','href="company.html#company"')
    f=f.replace('href="#promise"','href="index.html#promise"').replace('href="#support"','href="service.html"').replace('href="#cases"','href="cases.html"').replace('href="#flow"','href="flow.html"').replace('href="#faq"','href="contact.html#faq"').replace('href="#contact"','href="contact.html"')
    f=f.replace('<li><a href="contact.html#faq">よくあるご質問</a></li>','<li><a href="contact.html#faq">よくあるご質問</a></li><li><a href="partners.html">仲介会社・金融機関の方へ</a></li><li><a href="news.html">お知らせ</a></li><li><a href="column.html">コラム</a></li>')
    f=f.replace('<a href="index.html">プライバシーポリシー</a>','<a href="privacy.html">プライバシーポリシー</a>').replace('<a href="index.html">サイトのご利用について</a>','<a href="terms.html">サイトのご利用について</a>')
    return f
def page(fname,title,body,desc):
    t='工務店・住宅会社のM&A・事業承継｜株式会社エッジアセット' if fname=='index.html' else f'{title}｜株式会社エッジアセット'
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{'website' if fname=='index.html' else 'article' if fname.startswith('column-') else 'website'}">
<meta property="og:site_name" content="株式会社エッジアセット">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{U('rD28m9BmXVs')}">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
{JSONLD if fname=='index.html' else ''}
{head_links}
<style>{STYLE}</style>
</head>
<body{' class="home"' if fname=="index.html" else ""}>
{nav()}
<main id="top">
{body}
</main>
{footer()}
<div class="proto">デザイン確認用｜【 】内と写真は仮</div>
<script>{PREVIEW_FIX}</script>
<script>{SCRIPT}</script>
</body>
</html>
"""
def tolinks(x):
    return x.replace('href="#contact"','href="contact.html"').replace('href="#cf"','href="contact.html#cf"').replace('href="#faq"','href="contact.html#faq"')

# ---------- top page hero (split layout) ----------
fv_slides=''.join(f'<div class="slide ph{" on" if i==0 else ""}">{img(pid,alt,2400,i>0)}</div>' for i,(pid,alt,_) in enumerate(hero_slides))
FV=f"""<section class="fv" aria-label="メインビジュアル">
  <div class="fv-copy">
    <p class="fv-kick">工務店・住宅会社の事業承継</p>
    <h1>{W('地域の|工務店を、|つぎの|三十年へ。')}</h1>
    {P('建てた家の点検に、三十年後も伺える会社であるために。エッジアセットは、後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営します。','fv-lead')}
    <div class="fv-act"><a class="btn btn-navy" href="contact.html">事業承継について相談する {AR}</a><a class="tl" href="partners.html">仲介会社・金融機関の方へ {AR}</a></div>
    <ul class="fv-pts">
      <li><b>{W('売却を|前提に|しない')}</b><span>{W('グループ入り後も|長く保有')}</span></li>
      <li><b>{W('社名と雇用を|契約で守る')}</b><span>{W('施主様の|アフターも継続')}</span></li>
      <li><b>{W('秘密厳守で|面談')}</b><span>{W('社外・|オンラインで対応')}</span></li>
    </ul>
  </div>
  <div class="fv-pics">
    {fv_slides}
    <div class="fv-bar"><span class="pager" id="pager"><span id="cnt">01</span></span><a class="fv-news" href="news.html"><b>NEWS</b><time datetime="2026-10-22">2026.10.22</time><span>コーポレートサイトを公開しました</span></a></div>
  </div>
</section>"""

# ---------- new sections ----------
TBD='<em class="tbd">【確定後に記載】</em>'
TEAM=f"""<section class="team" id="team">
  <div class="w">
    {head('Team','メンバー','住宅業界の|実務を|知る人間が、|引き継ぎます','会社を託す相手は、ファンドの名前ではなく人です。グループ入り後に一緒に現場へ入るメンバーをご紹介します。')}
    <div class="tg">
      <article class="tm lead rv"><div class="ph tph">{img('rD28m9BmXVs','代表写真（撮影予定）',1000)}<span>写真は撮影予定</span></div><div class="tx"><p class="role">代表取締役</p><h3>谷岡 佑亮</h3><p class="en-name">Yusuke Tanioka</p>{P('株式会社船井総合研究所にて、上位0.5%の年間粗利獲得実績を複数年にわたり達成。経営再建・成長戦略の実行支援を経て、建築業界を中心に人材採用・営業体制の構築・業務改善を支援してきた。')}<a class="tl" href="#profile">プロフィールを見る {AR}</a></div></article>
      <article class="tm rv"><div class="ph tph empty"><span>写真</span></div><div class="tx"><p class="role">取締役／グループ経営支援</p><h3>{TBD}</h3>{P('集客・採用・財務の実務を担当します。')}</div></article>
      <article class="tm rv"><div class="ph tph empty"><span>写真</span></div><div class="tx"><p class="role">顧問（税理士）</p><h3>{TBD}</h3>{P('事業承継税制・株価算定を担当します。')}</div></article>
      <article class="tm rv"><div class="ph tph empty"><span>写真</span></div><div class="tx"><p class="role">顧問（弁護士）</p><h3>{TBD}</h3>{P('株式譲渡契約・許認可を担当します。')}</div></article>
    </div>
  </div>
</section>"""
CAPITAL=f"""<section class="capital dark" id="capital">
  <div class="w">
    {head('Capital','資金と体制','買い取る|資金と、|支え続ける|体制','一社目の譲渡を迷わず決めていただけるよう、資金の裏付けと支援体制を明らかにしています。')}
    <div class="cap3">
      <div class="rv"><p class="k">投資枠</p><p class="v">{TBD}</p>{P('工務店・住宅会社の株式取得に充てる自己資金と借入枠の合計です。','d')}</div>
      <div class="rv"><p class="k">提携金融機関</p><p class="v">{TBD}</p>{P('買収資金と、グループ会社の運転資金を支えます。','d')}</div>
      <div class="rv"><p class="k">専門家ネットワーク</p><p class="v">税理士・弁護士・M&amp;A実務</p>{P('株価算定、契約、許認可、労務までを社内外の専門家で対応します。','d')}</div>
    </div>
    <p class="capnote">エッジアセットは、外部の投資家から資金を集めて<span class="nb">運用するファンドではありません。</span><br>{TBD}</p>
  </div>
</section>"""
RECORD=f"""<section class="record" id="record">
  <div class="w rec">
    <div class="rv">{head('Track record','実績','グループ|1社目の|パートナーを|募集しています')}</div>
    <div class="rv">
      {P('エッジアセットは、2026年に設立した新しい会社です。現時点で、グループに入っていただいた会社はまだありません。')}
      {P('だからこそ、1社目の会社には、代表が直接、毎週関わります。グループの仕組みは、1社目の社長と一緒につくっていきます。')}
      <dl class="recdl"><div><dt>グループ会社数</dt><dd>0社（2026年10月時点）</dd></div><div><dt>検討中のご相談</dt><dd><em class="tbd">【確定後に記載】</em></dd></div></dl>
      <a class="btn btn-navy" href="contact.html">1社目について相談する {AR}</a>
    </div>
  </div>
</section>"""
CRIT=f"""<section class="crit" id="criteria">
  <div class="w">
    {head('Criteria','投資の目安','ご紹介いただきたい|会社の目安','目安に当てはまらない会社でも、住まいに関わる会社であればまずはお話を伺います。検討の可否は、理由とあわせてお伝えします。')}
    <table class="ctbl rv">
      <tr><th>事業内容</th><td>注文住宅・規格住宅・リフォーム・リノベーション（設計事務所、不動産兼業も可）</td></tr>
      <tr><th>所在地</th><td>全国（首都圏・東海・関西を優先）</td></tr>
      <tr><th>売上規模</th><td>年商3億〜30億円を目安（これ以外も検討します）</td></tr>
      <tr><th>収益</th><td>赤字でも、改善の見通しが立てば検討します</td></tr>
      <tr><th>取得の方法</th><td>株式譲渡（原則として全株式。一部取得もご相談ください）</td></tr>
      <tr><th>社長の処遇</th><td>続投・会長就任・引退のいずれも可能です</td></tr>
      <tr><th>保有方針</th><td>売却を前提にせず、長期で保有・経営します</td></tr>
    </table>
  </div>
</section>"""
PROMISE_P=f"""<section class="pp">
  <div class="w">
    {head('For partners','ご紹介者さまへのお約束','ご紹介いただいた|案件に、|誠実に|お応えします')}
    <div class="pp3">
      <div class="rv"><p class="n">01</p><h3>{W('初回のご回答は|5営業日以内')}</h3>{P('ノンネーム情報をいただいてから5営業日以内に、検討を進めるかどうかをご回答します。')}</div>
      <div class="rv"><p class="n">02</p><h3>{W('見送る場合も|理由をお伝えします')}</h3>{P('検討を見送る場合も、理由を具体的にお伝えします。売り手の方へのご説明にお使いください。')}</div>
      <div class="rv"><p class="n">03</p><h3>{W('既存の契約を|尊重します')}</h3>{P('仲介契約・FA契約の内容を尊重し、売り手の方との直接のやり取りはご紹介者さまを通じて行います。')}</div>
    </div>
  </div>
</section>"""
PFLOW=f"""<section class="pflow">
  <div class="w">
    {head('Process','ご紹介の流れ','ご紹介から|クロージングまで')}
    <ol class="steps">{''.join(f'<li class="rv"><h3>{W(h)}</h3><span class="t">{t}</span>{P(d)}</li>' for h,t,d in [('ノンネーム情報の|ご共有','Day 0','エリア・事業内容・規模がわかる範囲で構いません。'),('初回のご回答','5営業日','検討を進めるかどうかと、その理由をお伝えします。'),('秘密保持契約・|資料の検討','2〜4週間','決算書等をもとに、譲渡価格の考え方を整理します。'),('意向表明','2〜3週間','価格・雇用・社長の処遇を書面でご提示します。'),('詳細調査','1〜2ヶ月','財務・法務・労務・許認可・施工中物件を確認します。'),('最終契約・|クロージング','約1ヶ月','株式譲渡契約の締結と、代金のお支払いを行います。')])}</ol>
  </div>
</section>"""
PCONTACT=f"""<section class="pcon dark">
  <div class="w pc2">
    <div class="rv">{head('Contact','ご紹介の窓口','案件のご紹介・|ご相談は|こちらへ')}</div>
    <div class="rv"><dl class="pdl"><div><dt>担当</dt><dd>代表取締役　谷岡 佑亮</dd></div><div><dt>メール</dt><dd><em class="tbd">【確定後に記載】</em></dd></div><div><dt>電話</dt><dd>03-0000-0000（平日 9:00–18:00）</dd></div></dl><a class="btn btn-white" href="contact.html">フォームから連絡する {AR}</a></div>
  </div>
</section>"""
news_items=[('2026.10.22','お知らせ','コーポレートサイトを公開しました。')]
NEWS=f"""<section class="newslist">
  <div class="w">
    <ul class="nl-list">{''.join(f'<li><time>{d}</time><span class="cat">{c}</span><p>{t}</p></li>' for d,c,t in news_items)}</ul>
  </div>
</section>"""
TOPNEWS=f"""<section class="topnews">
  <div class="w tn">
    <div>{head('News','お知らせ','')}</div>
    <div><ul class="nl-list">{''.join(f'<li><time>{d}</time><span class="cat">{c}</span><p>{t}</p></li>' for d,c,t in news_items)}</ul><a class="tl" href="news.html">お知らせ一覧へ {AR}</a></div>
  </div>
</section>""".replace('<h2></h2>','')
TOPLINKS=f"""<section class="links">
  <div class="w l3">
    <a class="lk rv" href="company.html"><div class="ph">{img('rD28m9BmXVs','',1200)}</div><p class="len">About us</p><h3>私たちについて</h3><span>代表・メンバー・資金と体制・実績</span></a>
    <a class="lk rv" href="partners.html"><div class="ph">{img('4mEyvORkbN0','',1200)}</div><p class="len">For partners</p><h3>仲介会社・金融機関の皆さまへ</h3><span>投資の目安・ご紹介の流れ・窓口</span></a>
    <a class="lk rv" href="contact.html"><div class="ph">{img('Q6sCJFHCubc','',1200)}</div><p class="len">Contact</p><h3>ご相談・お問い合わせ</h3><span>面談の予約・電話・匿名でのご相談</span></a>
  </div>
</section>"""

# ---------- pages ----------
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'more.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pages2.py')).read())
home=FV+TRUST+tolinks(sec['market'])+ISSUES+tolinks(sec['stance'])+MODEL+tolinks(sec['promise'])+TOPCOST+tolinks(sec['people'].replace(sec['people'][sec['people'].index('<div class="frame">'):sec['people'].index('<div class="pg">')],'')+sec['cta'])+TOPCASES+tolinks(sec['flow'].replace('<div class="open">',f'<div class="fl-more"><a class="btn btn-navy" href="flow.html"{NT}>ご相談の流れを詳しく見る {AR}</a></div><div class="open">'))+TOPSEO+TOPFAQ+TOPCOL+TOPNEWS
home=home.replace('<div class="btns" style="margin-top:44px"><a class="btn btn-navy" href="contact.html">似た状況について相談する','<div class="btns" style="margin-top:44px"><a class="btn btn-navy" href="contact.html">似た状況について相談する')
company=phero('About us','私たちについて','後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営する。エッジアセットの考え方と、それを支える人・資金・体制をご紹介します。','rD28m9BmXVs')+subnav([('about','考え方'),('message','代表メッセージ'),('profile','代表プロフィール'),('team','体制'),('capital','資金と体制'),('record','実績'),('compare','他の選択肢との比較'),('company','会社概要')])+tolinks(sec['about'].replace('<a class="tl" href="#support">','<a class="tl" href="service.html">').replace('<p class="sh-en" aria-hidden="true">About</p><p class="sh-ja">私たちについて</p>','<p class="sh-en" aria-hidden="true">Philosophy</p><p class="sh-ja">私たちの考え方</p>')+sec['msg'])+PROFILE+COMPANY_BAND+VMV+TEAM2+CAPITAL+GOV+RECORD+tolinks(sec['compare'])+HISTORY+tolinks(sec['company'])+CLOSE_CO+nextlink('service.html','Our support','グループの支援')
partners=phero('For partners','仲介会社・金融機関の皆さまへ','住宅会社の事業承継案件のご紹介をお待ちしています。投資の目安、ご紹介の流れ、窓口をまとめました。','4mEyvORkbN0')+CRIT+PROMISE_P+INFO+PFLOW+PFAQ+PCONTACT+nextlink('cases.html','Model cases','モデルケース')
news=phero('News','お知らせ','','Q6sCJFHCubc')+NEWS+CLOSE+nextlink('company.html','About us','私たちについて')
contact=phero('Contact','ご相談・お問い合わせ','ご相談は無料です。社名を伏せたままでも構いません。','Q6sCJFHCubc')+re.sub(r'<div class="ph side">.*?</div>',CONTACT_ASIDE,sec['contact'],count=1,flags=re.S)+PREP+sec['faq']
service=phero('Our support','グループの支援','家づくりの方針には口を出さず、規模が小さいほど負担が重くなる仕事をグループで引き受けます。','4UVtFIfK1eo')+subnav([('support','支援の内容'),('cost','原価の改善'),('model','グループの仕組み'),('before','グループ入りの前と後'),('d100','最初の100日'),('svcfaq','よくあるご質問')])+SERVICE_INTRO+SVC_KPI+tolinks(sec['support'])+COST+SERVICE_BAND+MODEL+BEFORE.replace('<section class="ba"','<section class="ba" id="before"',1)+re.sub(r'<section class="([^"]*)"',r'<section class="\1" id="d100"',D100,count=1)+SVCFAQ.replace('<section class="topfaq"','<section class="topfaq" id="svcfaq"',1)+CLOSE_SVC+nextlink('cases.html','Model cases','モデルケース')
bodies={'service.html':(service,'エッジアセットがグループで担う支援：集客・採用・財務・仕入・業務・人材。グループ入り後の100日。'),'index.html':(home,'株式会社エッジアセットは、後継者が決まっていない工務店・住宅会社を引き継ぎ、売らずに長く経営する事業承継の受け皿です。'),
 'company.html':(company,'エッジアセットの考え方、代表メッセージ、メンバー、資金と体制、実績、会社概要。'),
 'partners.html':(partners,'仲介会社・金融機関の皆さまへ。投資の目安、ご紹介の流れ、窓口。'),
 'news.html':(news,'エッジアセットからのお知らせ。'),
 'contact.html':(contact,'工務店・住宅会社の事業承継のご相談・お問い合わせ。')}
EXTRA_CSS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'extra.css')).read()
STYLE=css_main+'\n'+EXTRA_CSS
SCRIPT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'site.js')).read()
# when viewed through htmlpreview.github.io, keep page-to-page links inside the preview
PREVIEW_FIX="""if(location.hostname==='htmlpreview.github.io'){var base=location.search.slice(1).replace(/[^/]*$/,'');document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href');if(/^(https?:|mailto:|tel:|#|\\/\\/)/.test(h))return;e.preventDefault();var p=h.split('#');var u=location.pathname+'?'+base+p[0]+(p[1]?'#'+p[1]:'');if(a.target==='_blank'){window.open(u,'_blank','noopener')}else{location.href=u}});}"""
TEL='03-0000-0000'
def telify(html):
    html=html.replace('<i>'+TEL+'</i>','<i>@@TEL@@</i>')  # already inside a link
    html=re.sub(r'<a [^>]*href="tel:[^"]*"[^>]*>.*?</a>',lambda m:m.group(0).replace(TEL,'@@TEL@@'),html,flags=re.S)  # existing tel: links
    html=re.sub(r'(?<![\w"=:/.-])'+re.escape(TEL)+r'(?![\w-])','<a class="tel-a" href="tel:0300000000">'+TEL+'</a>',html)
    return html.replace('@@TEL@@',TEL)
for a in ARTICLES:
    PAGES.append((a['slug'],a['title']))
    bodies[a['slug']]=(article_page(a),a['lead'][:110])
PAGES+= [('cases.html','モデルケース'),('flow.html','ご相談の流れ')]
bodies['cases.html']=(phero('Model cases','モデルケース','よくいただくご相談を、引き継ぎの形と、グループ入り後の1年まで含めてまとめました。','TJ4CndIc9z8')+CASELIST+CASES_BAND+CLOSE_CASE+nextlink('flow.html','Flow','ご相談の流れ'),'工務店・住宅会社の事業承継のモデルケース。後継者不在、成長の壁、廃業の検討、粗利の低下。')
bodies['flow.html']=(phero('Flow','ご相談の流れ','初回面談から最終契約まで通常は半年前後、その後半年ほどかけて引き継ぎます。各段階でやること、ご用意いただくもの、話が伝わる範囲をまとめました。','Q6sCJFHCubc')+FLOWPAGE+FLOW_BAND+CLOSE_FLOW+nextlink('contact.html','Contact','ご相談・お問い合わせ'),'工務店・住宅会社の事業承継、ご相談から引き継ぎまでの流れ。')
for i,c in enumerate(CASES):
    PAGES.append((c['slug']+'.html','モデルケース '+f'{i+1:02d}｜'+c['tag']))
    bodies[c['slug']+'.html']=(case_page(c,i),c['short'])
PAGES+= [('column.html','コラム'),('privacy.html','プライバシーポリシー'),('terms.html','サイトのご利用について'),('404.html','ページが見つかりません')]
bodies['column.html']=(phero('Column','コラム','工務店・住宅会社の事業承継について、社長が判断に迷うポイントを解説しています。','Q6sCJFHCubc')+COLLIST,'工務店・住宅会社の事業承継に関するコラム。')
bodies['privacy.html']=(PRIVACY,'株式会社エッジアセットのプライバシーポリシー。')
bodies['terms.html']=(TERMS,'株式会社エッジアセットのサイトのご利用について。')
bodies['404.html']=(NOTFOUND,'お探しのページは見つかりませんでした。')
for fname,title in PAGES:
    b,d=bodies[fname]
    open(os.path.join(OUT,fname),'w').write(telify(page(fname,title,b,d)))
SITE='https://www.example.com/'  # 本番ドメインが決まったら差し替え
open(os.path.join(OUT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE}{'' if f=='index.html' else f}</loc></url>\n' for f,_ in PAGES if f!='404.html')+'</urlset>\n')
open(os.path.join(OUT,'robots.txt'),'w').write('User-agent: *\nAllow: /\nSitemap: '+SITE+'sitemap.xml\n')
open(os.path.join(OUT,'favicon.svg'),'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0c2747"/><text x="32" y="42" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="26" font-weight="600" letter-spacing="1" fill="#fff">EA</text></svg>\n')

print('pages written')
