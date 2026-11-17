# Copy only what the built site uses into dist/ for Firebase Hosting.
# usage: py tools/dist.py   (run from edge-asset/ after build)
import re,glob,os,shutil
shutil.rmtree('dist',ignore_errors=True); os.makedirs('dist')
files=set(glob.glob('*.html'))|{'site.css','site.js','favicon.svg','apple-touch-icon.png','robots.txt','sitemap.xml'}
for f in [f for f in files if f.endswith(('.html','.css'))]:
    files|={m for m in re.findall(r'(img/[\w./-]+\.(?:jpg|jpeg|png|svg|webp))',open(f,encoding='utf-8').read()) if os.path.isfile(m)}
for f in files:
    os.makedirs(os.path.join('dist',os.path.dirname(f)),exist_ok=True); shutil.copy(f,os.path.join('dist',f))
print(len(files),'files')
