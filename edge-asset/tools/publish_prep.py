# Copy the built site into a publish folder and unwrap index.html for the Artifact preview.
# usage: python3 tools/publish_prep.py <out_dir>   (run from edge-asset/ after build)
import re,sys,shutil,glob,os
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
for f in glob.glob(os.path.join(out,'*.html')): os.remove(f)
for f in glob.glob('*.html')+['site.css','favicon.svg']: shutil.copy(f,out)
p=os.path.join(out,'index.html'); s=open(p,encoding='utf-8').read()
s=re.sub(r'<!doctype html>','',s,flags=re.I)
s=re.sub(r'<title>.*?</title>','<title>エッジアセット コーポレートサイト</title>',s,flags=re.S)
s=re.sub(r'</?html[^>]*>|</?head>','',s)
s=re.sub(r'<body[^>]*>','<script>document.body.classList.add("home")</script>',s,count=1)
s=s.replace('</body>','')
open(p,'w',encoding='utf-8').write(s)
print('files:',sorted(os.path.basename(f) for f in glob.glob(os.path.join(out,'*')) if os.path.isfile(f)))
