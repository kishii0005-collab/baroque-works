import {execFileSync} from 'child_process';
import pw from '/opt/node-tools/node_modules/playwright/index.js'; const { chromium } = pw;
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const [pg,w,...ys]=process.argv.slice(2);
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:+w,height:900}});
await p.route(/unsplash|wsrv/, r=>r.abort());
await p.route(/fonts\.(googleapis|gstatic)\.com/, r=>{const u=r.request().url(); const body=execFileSync('curl',['-sS','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',u]); r.fulfill({status:200,body,headers:{'content-type':u.includes('css')?'text/css':'font/woff2','access-control-allow-origin':'*'}});});
await p.goto(`file:///home/user/baroque-works/edge-asset/${pg}.html`,{waitUntil:'load'}); await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>document.fonts.check('600 20px "Zen Old Mincho"')), await p.evaluate(()=>document.body.scrollHeight));
for (const y of ys){ await p.evaluate(y=>scrollTo(0,y),+y); await p.waitForTimeout(1300); await p.screenshot({path:`d4_${pg}_${w}_${y}.png`}); }
await b.close();
