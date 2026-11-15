import pw from '/opt/node-tools/node_modules/playwright/index.js'; const { chromium } = pw;
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const fs = await import('fs'); const png = fs.readFileSync('/home/user/baroque-works/edge-asset/img/Q6sCJFHCubc.jpg');
const pages=['index','company','service','results','cases','case-5','flow','partners','faq','contact','valuation','column','column-1','news','sitemap','privacy','404'];
for (const pg of pages) for (const w of [1440,390]) {
  const p = await b.newPage({viewport:{width:w,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route(/unsplash|wsrv/, r=>r.fulfill({status:200,contentType:'image/jpeg',body:png}));
  await p.route(/googleapis|gstatic/, r=>r.abort());
  await p.goto(`file:///home/user/baroque-works/edge-asset/${pg}.html`);
  for (let y=0;y<30000;y+=500){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(40); }
  await p.waitForTimeout(1200);
  const r = await p.evaluate(()=>{
    const bad=[];
    document.querySelectorAll('h1,h2,h3,.lead,.plead,.fv-lead,p,summary span,li,dd').forEach(el=>{
      if(el.children.length>3) return;
      const tw=document.createTreeWalker(el,NodeFilter.SHOW_TEXT); const chars=[];let n;
      while(n=tw.nextNode()){for(let i=0;i<n.length;i++){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const rc=r.getClientRects()[0];if(rc&&rc.width>0)chars.push([rc.top,n.data[i]]);}}
      const keys=[],lines={};chars.forEach(([t,c])=>{let k=keys.find(x=>Math.abs(x-t)<8);if(k===undefined){k=t;keys.push(t)}lines[k]=(lines[k]||'')+c});
      const ls=Object.values(lines); if(ls.length>1){const s=ls.slice().sort((a,b)=>a.trim().length-b.trim().length)[0].trim(); if(s.replace(/[。、」）]/g,'').length<=2) bad.push(ls.join(' / '));}
    });
    const im=[...document.querySelectorAll('.ph img')];
    return {sw:document.documentElement.scrollWidth, imgs:im.length, shown:im.filter(i=>i.naturalWidth>0&&getComputedStyle(i).visibility!=='hidden').length, hiddenRv:[...document.querySelectorAll('.rv')].filter(e=>!e.classList.contains('in')).length, bad:[...new Set(bad)].slice(0,6)};
  });
  console.log(pg,w,JSON.stringify(r),errs.length?errs:'');
  if (process.env.SHOTS) await p.screenshot({path:`pg_${pg}_${w}.png`, fullPage:true});
  await p.close();
}
await b.close();
