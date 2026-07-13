import json, os, html as htm

base = r'C:\Users\ckyeung\OneDrive\桌面\賺錢\hinfok\main'
ad = os.path.join(base, 'src', 'articles')
cd = os.path.join(base, 'src', 'data')
out = os.path.join(base, 'output')
os.makedirs(out, exist_ok=True)

config = json.load(open(os.path.join(cd, 'config.json'), encoding='utf-8'))
cats = json.load(open(os.path.join(cd, 'categories.json'), encoding='utf-8'))['categories']
S = config['site']; SE = config['seo']
ADS = config.get('adsense', {'enabled': False, 'publisherId': ''})
ADS_ID = ADS.get('publisherId', '') if ADS.get('enabled') else ''

articles = []
for f in os.listdir(ad):
    if f.endswith('.json') and f not in ['privacy.json','about.json']:
        articles.append(json.load(open(os.path.join(ad, f), encoding='utf-8')))

by_cat = {}
for art in articles:
    by_cat.setdefault(art.get('category','other'), []).append(art)

search_idx = []
for art in articles:
    cn = ''
    for c in cats:
        if c['id'] == art.get('category',''): cn = c['name']; break
    search_idx.append({'slug':art['slug'],'title':art['title'],'summary':art['summary'][:200],'keywords':art['seo']['keywords'],'category':art.get('category',''),'cat_name':cn})

json.dump(search_idx, open(os.path.join(out, 'article-index.json'), 'w', encoding='utf-8'), ensure_ascii=False)

ch = chr
def esc(s): return htm.escape(s).replace(ch(10), ' ')

html = []
html.append('<!DOCTYPE html>')
html.append('<html lang="zh-HK">')
html.append('<head>')
html.append('<meta charset="UTF-8">')
html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
html.append('<meta name="description" content="' + esc(SE['defaultDescription']) + '">')
html.append('<meta property="og:title" content="HKInformation 香港資訊數據圖鑑 — 用數據看懂香港">')
html.append('<meta property="og:description" content="' + esc(SE['defaultDescription']) + '">')
html.append('<meta property="og:type" content="website">')
html.append('<meta property="og:site_name" content="' + esc(S['name']) + '">')
html.append('<link rel="canonical" href="' + S['baseUrl'] + '/">')
html.append('<meta name="robots" content="index, follow">')
if SE.get('googleSiteVerification'):
    html.append('<meta name="google-site-verification" content="' + SE['googleSiteVerification'] + '">')
if ADS_ID:
    html.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADS_ID + '" crossorigin="anonymous"></script>')

html.append('<title>HKInformation 香港資訊數據圖鑑 — 用數據看懂香港</title>')
jld = {"@context":"https://schema.org","@type":"WebSite","name":S['name'],"url":S['baseUrl'],"description":SE['defaultDescription'],"potentialAction":{"@type":"SearchAction","target":S['baseUrl']+'/?s={search_term_string}',"query-input":"required name=search_term_string"}}
html.append('<script type="application/ld+json">' + json.dumps(jld, ensure_ascii=False) + '</script>')

# CSS
html.append('<style>')
html.append('*{margin:0;padding:0;box-sizing:border-box}')
html.append('body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif;background:#f0f4f8;color:#1a2332;line-height:1.7}')
html.append('header{background:linear-gradient(135deg,#1e3a5f,#2d5a87);color:#fff;position:sticky;top:0;z-index:100;box-shadow:0 2px 20px rgba(0,0,0,0.15)}')
html.append('.hdr{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:60px}')
html.append('.nav-links{display:flex;gap:4px;list-style:none;margin:0;padding:0}')
html.append('.nav-links a{color:rgba(255,255,255,0.85);text-decoration:none;padding:6px 10px;border-radius:6px;font-size:13px;white-space:nowrap;transition:.2s}')
html.append('.nav-links a:hover{background:rgba(255,255,255,0.12)}')
html.append('.nav-toggle{display:none;background:none;border:none;color:#fff;font-size:24px;cursor:pointer}')
html.append('@media(max-width:768px){.nav-links{display:none;position:absolute;top:60px;left:0;right:0;background:#1e3a5f;padding:16px;flex-direction:column}.nav-links.open{display:flex}.nav-toggle{display:block}.hdr{flex-wrap:wrap}.sbw{order:3}}')
html.append('.logo{font-size:20px;font-weight:800;color:#fff;text-decoration:none}')
html.append('.logo span{color:#f4a261}')
html.append('.sbw{position:relative;max-width:250px}')
html.append('.sbw input{width:100%;padding:8px 12px;border:none;border-radius:8px;font-size:13px;background:rgba(255,255,255,0.15);color:#fff;outline:none}')
html.append('.sbw input::placeholder{color:rgba(255,255,255,0.5)}')
html.append('.sbw input:focus{background:rgba(255,255,255,0.25)}')
html.append('.sr{position:absolute;top:100%;right:0;width:350px;background:#fff;border-radius:8px;box-shadow:0 8px 30px rgba(0,0,0,0.15);max-height:350px;overflow-y:auto;display:none;z-index:200}')
html.append('.sr a{display:block;padding:10px 14px;text-decoration:none;color:#333;border-bottom:1px solid #eee;font-size:13px}')
html.append('.sr a:hover{background:#f0f4f8};.sr .c{font-size:11px;color:#888}')
html.append('.hero{background:linear-gradient(135deg,#1e3a5f,#2d5a87 50%,#457b9d);color:#fff;padding:50px 24px;text-align:center}')
html.append('.hero h1{font-size:34px;margin-bottom:8px;font-weight:800}')
html.append('.hero p{font-size:16px;opacity:.85;margin:0 auto 24px;max-width:600px}')
html.append('.sts{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-bottom:24px}')
html.append('.st{text-align:center}')
html.append('.st .n{font-size:26px;font-weight:800}')
html.append('.st .l{font-size:13px;opacity:.7}')
html.append('.hsb{max-width:480px;margin:0 auto;position:relative}')
html.append('.hsb input{width:100%;padding:12px 18px;border:none;border-radius:10px;font-size:15px;outline:none;box-shadow:0 4px 20px rgba(0,0,0,0.2)}')
html.append('.hsr{position:absolute;top:100%;left:0;right:0;background:#fff;border-radius:0 0 10px 10px;box-shadow:0 8px 30px rgba(0,0,0,0.15);max-height:320px;overflow-y:auto;display:none}')
html.append('.hsr a{display:block;padding:12px 18px;text-decoration:none;color:#333;border-bottom:1px solid #eee;font-size:14px}')
html.append('.hsr a:hover{background:#f0f4f8};.hsr .c{font-size:11px;color:#888}')
html.append('.sc{max-width:1200px;margin:0 auto;padding:32px 24px}')
html.append('.sc h2{font-size:22px;color:#1e3a5f;margin-bottom:8px}')
html.append('.sc p{color:#888;font-size:14px;margin-bottom:16px}')
html.append('.cg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}')
html.append('.cd{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.06);display:flex;flex-direction:column;text-decoration:none;color:inherit;transition:.2s}')
html.append('.cd:hover{transform:translateY(-3px);box-shadow:0 6px 24px rgba(0,0,0,0.1)}')
html.append('.cdb{padding:14px 16px;flex:1;display:flex;flex-direction:column}')
html.append('.cdb h3{font-size:15px;color:#1e3a5f;margin-bottom:6px;line-height:1.3}')
html.append('.cdb p{font-size:13px;color:#555;flex:1}')
html.append('.tag{display:inline-block;background:#e8edf3;color:#1e3a5f;padding:2px 8px;border-radius:12px;font-size:11px;margin:4px 2px 0 0}')
html.append('footer{background:#1a2332;color:rgba(255,255,255,0.7);padding:28px 24px;text-align:center;font-size:13px}')
html.append('footer a{color:#f4a261;text-decoration:none}')
html.append('@media(max-width:900px){.cg{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:28px}}')
html.append('@media(max-width:650px){.cg{grid-template-columns:1fr}.hero h1{font-size:22px}.hdr{height:auto;padding:12px 16px;flex-wrap:wrap}.sbw{max-width:100%;width:100%;order:3}}')
html.append('</style></head><body>')

# Header
html.append('<header><div class="hdr">')
html.append('<a href="/" class="logo">HK<span>Info</span> 香港資訊數據圖鑑</a>')
html.append('<div class="sbw"><input type="text" id="hs" placeholder="搜尋..." oninput="q(this.value,1)"><div id="sr1" class="sr"></div></div>')
html.append('<nav class="nav-links">')
html.append('<a href="/#cat-housing">樓市與房屋</a>')
html.append('<a href="/#cat-population">人口與社會</a>')
html.append('<a href="/#cat-economy">經濟與零售</a>')
html.append('<a href="/#cat-labour">職場與教育</a>')
html.append('<a href="/#cat-culture">文化與交通</a>')
html.append('<a href="/#cat-medical">醫療與環境</a>')
html.append('</nav>')
# nav toggle
html.append('<button class="nav-toggle" onclick="var n=document.querySelector(\'.nav-links\');if(n)n.classList.toggle(\'open\')">\u2630</button>')

html.append('</div></header>')

# Hero
html.append('<section class="hero">')
html.append('<h1>HKInformation 香港資訊數據圖鑑</h1>')
html.append('<p>' + S['tagline'] + '</p>')
html.append('<div class="sts">')
html.append('<div class="st"><div class="n">30+</div><div class="l">分析文章</div></div>')
html.append('<div class="st"><div class="n">6</div><div class="l">大分類</div></div>')
html.append('<div class="st"><div class="n">2015-2025</div><div class="l">十年數據</div></div>')
html.append('</div>')
html.append('<div class="hsb"><input type="text" id="hs2" placeholder="搜尋分析文章，例如樓價、出生率、通脹..." oninput="q(this.value,2)"><div id="sr2" class="hsr"></div></div>')
html.append('</section>')

# Categories
for c in cats:
    cid = c['id']; arts = by_cat.get(cid, [])
    if not arts: continue
    html.append('<section class="sc" id="cat-' + cid + '">')
    html.append('<h2>' + c.get('icon','') + ' ' + c['name'] + '</h2>')
    html.append('<p>' + c.get('desc','') + '</p><div class="cg">')
    for art in arts[:6]:
        kw = ''.join('<span class="tag">' + k.strip() + '</span>' for k in art['seo']['keywords'].split(',')[:2])
        html.append('<a href="/' + art['slug'] + '" class="cd"><div class="cdb">')
        html.append('<h3>' + esc(art['title'][:60]) + '</h3>')
        html.append('<p>' + esc(art['summary'][:150]) + '...</p>')
        if kw: html.append('<div>' + kw + '</div>')
        html.append('</div></a>')
    html.append('</div></section>')

# Footer
html.append('<footer>')
html.append('<p style="margin-bottom:12px"><a href="/about">關於我們</a> · <a href="/privacy">私隱政策</a> · <a href="/sitemap.xml">網站地圖</a></p>')
html.append('<p>' + S['name'] + '</p><p style="font-size:12px;opacity:0.7;max-width:700px;margin:8px auto">' + S['footer']['disclaimer'] + '</p><p style="margin-top:8px">' + S['footer']['copyright'] + '</p>')
html.append('</footer>')

# JS
html.append('<script>')
html.append('const idx=' + json.dumps(search_idx, ensure_ascii=False) + ';')
html.append('function q(v,t){const e=document.getElementById("sr"+t);if(!v||v.length<2){e.style.display="none";e.innerHTML="";return}')
html.append('const m=idx.filter(a=>a.title.includes(v)||a.summary.includes(v)).slice(0,6);')
html.append('if(m.length===0){e.innerHTML="<a style=\\"color:#999;cursor:default\\">無結果</a>";e.style.display="block";return}')
html.append('e.innerHTML=m.map(a=>"<a href=\'/" + a.slug + "\'>" + a.title + "<span class=\\"c\\">" + a.cat_name + "</span></a>").join("");e.style.display="block"}')
html.append('document.addEventListener("click",function(e){if(!e.target.closest(".sbw")&&!e.target.closest(".hsb")){document.querySelectorAll(".sr,.hsr").forEach(el=>{el.style.display="none"})}})')
html.append('</script>')
html.append('<div id="ck" style="position:fixed;bottom:0;left:0;right:0;background:#1a2332;color:#fff;padding:14px 20px;z-index:999;display:none;font-size:13px"><div style="max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap"><span>本網站使用 Cookie 以改善體驗及顯示廣告。繼續使用即表示同意我們的 <a href="/privacy" style="color:#f4a261">私隱政策</a>。</span><button onclick="document.getElementById(\'ck\').style.display=\'none\';localStorage.setItem(\'ck\',1)" style="background:#f4a261;border:none;color:#1a2332;padding:8px 20px;border-radius:6px;font-weight:600;cursor:pointer;white-space:nowrap">我了解</button></div></div>')
html.append('<script>if(!localStorage.getItem("ck")){document.getElementById("ck").style.display="block"}</script>')
html.append('</body></html>')

with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))
print('Index generated:', len(html), 'lines')