"""Fetch site photos from Wikimedia Commons (reachable from GitHub runners, unlike Unsplash).
1) For each Unsplash ID the site uses, look for the same photo mirrored on Commons.
2) For each theme, download a few free-licensed candidates so a replacement can be chosen.
Writes edge-asset/img/{id}.jpg for exact matches and edge-asset/img/candidates/*.jpg + meta.json."""
import json, os, re, time, urllib.error, urllib.parse, urllib.request
UA = 'EdgeAssetSiteBuilder/1.1 (https://github.com/kishii0005-collab/baroque-works; site photo fetch) python-urllib'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')
CAND = os.path.join(ROOT, 'candidates'); os.makedirs(CAND, exist_ok=True)
IDS = ['GpJ9p1QH7O4','q1tyQip5AQQ','a8A-z_ZPEC0','rD28m9BmXVs','Q6sCJFHCubc','-MVSfkR4xz4','TJ4CndIc9z8','pcYN7Pi8_BQ','4UVtFIfK1eo','4mEyvORkbN0']
THEMES = {
 'night':'Osaka night skyline', 'house':'Japanese modern house exterior', 'arch':'Yokohama modern architecture',
 'office':'Tokyo office buildings skyscrapers', 'street':'Tokyo residential street houses', 'green':'Japanese house garden trees',
 'town':'Japanese suburban houses', 'dusk':'Tokyo residential area dusk', 'frame':'timber frame house construction', 'meeting':'business handshake meeting'}
OK_LIC = re.compile(r'(cc0|public domain|pd|cc by|cc-by|unsplash)', re.I)
def fetch(url, timeout=60):
    for n in range(6):
        time.sleep(1.5)
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503): time.sleep(10 * (n + 1)); continue
            raise
    raise RuntimeError('rate limited: ' + url)
def api(**q):
    q.update(format='json', maxlag='5')
    return json.loads(fetch('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(q), 30))
def info(title):
    d = api(action='query', titles=title, prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth=2000)
    p = next(iter(d['query']['pages'].values())); ii = (p.get('imageinfo') or [None])[0]
    if not ii or ii.get('mime') != 'image/jpeg': return None
    m = ii.get('extmetadata', {})
    g = lambda k: re.sub('<[^>]+>', '', (m.get(k) or {}).get('value', ''))[:160]
    return dict(title=title, url=ii.get('thumburl') or ii['url'], page=ii.get('descriptionurl'), w=ii.get('width'), h=ii.get('height'),
                license=g('LicenseShortName'), artist=g('Artist'))
def get(url, path):
    data = fetch(url)
    if data[:3] != b'\xff\xd8\xff': raise ValueError('not jpeg')
    open(path, 'wb').write(data)
meta = {'exact': {}, 'candidates': {}}
for pid in IDS:
    try:
        r = api(action='query', list='search', srnamespace=6, srlimit=3, srsearch=f'"{pid}"')
        for hit in r['query']['search']:
            if pid in hit['title']:
                i = info(hit['title'])
                if i: get(i['url'], os.path.join(ROOT, f'{pid}.jpg')); meta['exact'][pid] = i; print('exact', pid, i['title']); break
        else: print('no exact', pid)
    except Exception as e: print('fail', pid, e)
for key, q in THEMES.items():
    try:
        r = api(action='query', list='search', srnamespace=6, srlimit=25, srsearch=q + ' filetype:bitmap')
        n = 0
        for hit in r['query']['search']:
            if n >= 4: break
            i = info(hit['title'])
            if not i or not OK_LIC.search(i['license'] or '') or (i['w'] or 0) < 1600 or (i['w'] or 0) < (i['h'] or 0): continue
            fn = f'{key}-{n+1}.jpg'; get(i['url'], os.path.join(CAND, fn)); meta['candidates'][fn] = i; n += 1
        print('theme', key, n)
    except Exception as e: print('fail theme', key, e)
json.dump(meta, open(os.path.join(CAND, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
