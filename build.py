import json, os, shutil, html
from pathlib import Path

BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
OUTPUT_DIR = BASE_DIR / "output"

def load_json(rel_path):
    with open(SRC_DIR / rel_path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_json("data/config.json")
SITE = config["site"]
NAV = config["nav"]
SEO = config["seo"]
THEME = config["theme"]
AUTHOR = config["author"]
ADSENSE = config.get("adsense", {"enabled": False, "publisherId": ""})
EMAIL = SITE.get("email", "")

HEADER_CSS = """
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; 
       background: #f0f4f8; color: #1a2332; line-height: 1.8; }
.site-header { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: #fff; padding: 0; position: sticky; top: 0; z-index: 50; box-shadow: 0 2px 20px rgba(0,0,0,0.15); }
.header-inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 64px; }
.site-logo { font-size: 22px; font-weight: 800; color: #fff; text-decoration: none; }
.site-logo span { color: #f4a261; }
.nav-links { display: flex; gap: 6px; list-style: none; }
.nav-links a { color: rgba(255,255,255,0.85); text-decoration: none; padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 500; transition: all 0.2s; }
.nav-links a:hover, .nav-links a.active { background: rgba(255,255,255,0.12); color: #fff; }
.nav-toggle { display: none; background: none; border: none; color: #fff; font-size: 28px; cursor: pointer; }
.hero { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: #fff; padding: 64px 24px; text-align: center; position: relative; overflow: hidden; }
.hero h1 { font-size: 32px; margin-bottom: 16px; line-height: 1.3; max-width: 800px; margin-left: auto; margin-right: auto; }
.hero p { font-size: 16px; opacity: 0.85; max-width: 650px; margin: 0 auto; }
.hero-img { width: 100%; max-height: 420px; object-fit: cover; border-radius: 12px; margin-top: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.2); }
.hero-caption { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 8px; text-align: center; }
.page-hero { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: #fff; padding: 48px 24px 32px; text-align: center; }
.page-hero h1 { font-size: 28px; margin-bottom: 8px; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.section { padding: 40px 0; }
.section h2 { font-size: 24px; margin-bottom: 20px; color: #1e3a5f; padding-bottom: 8px; border-bottom: 3px solid #e63946; display: inline-block; }
.section h3 { font-size: 18px; margin: 24px 0 12px; color: #2d5a87; }
.section p { margin-bottom: 16px; line-height: 1.9; color: #2c3e50; }
.chart-box { background: #fff; border-radius: 12px; padding: 20px; margin: 28px 0; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.chart-box h3 { font-size: 16px; color: #1e3a5f; margin-bottom: 12px; }
.data-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 8px rgba(0,0,0,0.05); }
.data-table th { background: #1e3a5f; color: #fff; padding: 12px 16px; text-align: left; font-weight: 600; }
.data-table td { padding: 10px 16px; border-bottom: 1px solid #eee; }
.data-table tr:nth-child(even) { background: #f8fafc; }
.summary-box { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: #fff; border-radius: 12px; padding: 28px; margin: 28px 0; }
.summary-box h3 { color: #f4a261; margin-bottom: 12px; font-size: 18px; }
.summary-box p { color: rgba(255,255,255,0.9); line-height: 1.8; }
.meta-info { display: flex; gap: 20px; flex-wrap: wrap; font-size: 13px; color: #666; margin: 16px 0; }
.meta-info a { color: #457b9d; }
.tag { display: inline-block; background: #e8edf3; color: #1e3a5f; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin: 2px; }
.related-card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-decoration: none; display: block; color: inherit; transition: transform 0.2s; }
.related-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.related-card h4 { color: #1e3a5f; font-size: 16px; margin-bottom: 8px; }
.related-card p { font-size: 13px; color: #666; line-height: 1.5; }
.site-footer { background: #1a2332; color: rgba(255,255,255,0.7); padding: 40px 24px 24px; margin-top: 48px; }
.footer-inner { max-width: 1100px; margin: 0 auto; }
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 32px; margin-bottom: 24px; }
.footer-grid h4 { color: #fff; font-size: 16px; margin-bottom: 12px; }
.footer-grid p { font-size: 13px; line-height: 1.7; }
.footer-grid ul { list-style: none; }
.footer-grid li { margin-bottom: 6px; }
.footer-grid a { color: rgba(255,255,255,0.6); text-decoration: none; font-size: 13px; }
.footer-grid a:hover { color: #f4a261; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 16px; font-size: 12px; text-align: center; }
.footer-bottom p { margin-bottom: 6px; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 16px; max-width: 1100px; margin-left: auto; margin-right: auto; padding: 0 24px; }
.breadcrumb a { color: #457b9d; text-decoration: none; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
@media (max-width: 768px) { 
    .nav-links { display: none; flex-direction: column; position: absolute; top: 64px; left: 0; right: 0; background: #1e3a5f; padding: 16px; z-index: 100; }
    .nav-links.open { display: flex; }
    .nav-toggle { display: block; }
    .hero h1 { font-size: 24px; }
    .grid-2, .grid-3 { grid-template-columns: 1fr; }
    .footer-grid { grid-template-columns: 1fr; }
}
.home-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06); transition: transform 0.2s; cursor: pointer; display: block; text-decoration: none; color: inherit; }
.home-card:hover { transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.1); }
.home-card-img { width: 100%; height: 180px; object-fit: cover; }
.home-card-body { padding: 20px; }
.home-card-body h3 { font-size: 18px; color: #1e3a5f; margin-bottom: 8px; }
.home-card-body p { font-size: 13px; color: #555; line-height: 1.6; }
.home-card-body .tags { margin-top: 10px; }
.index-hero { background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #457b9d 100%); color: #fff; padding: 80px 24px; text-align: center; }
.index-hero h1 { font-size: 42px; margin-bottom: 16px; }
.index-hero p { font-size: 18px; opacity: 0.85; max-width: 650px; margin: 0 auto; }
.stat-bar { background: #fff; border-radius: 12px; padding: 20px 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center; }
.stat-bar .num { font-size: 28px; font-weight: 800; color: #1e3a5f; }
.stat-bar .label { font-size: 13px; color: #888; }
.plain-content { background: #fff; border-radius: 12px; padding: 32px; margin: 24px 0; box-shadow: 0 1px 12px rgba(0,0,0,0.05); }
.plain-content ul, .plain-content ol { margin-left: 24px; line-height: 2; }
.plain-content a { color: #457b9d; }
#cookie-banner { position: fixed; bottom: 0; left: 0; right: 0; background: #1a2332; color: #fff; padding: 16px 24px; z-index: 999; display: none; font-size: 14px; line-height: 1.5; }
#cookie-banner a { color: #f4a261; }

.toc-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px 28px; margin:28px 0; }
.toc-box h3 { font-size:16px; color:#1e3a5f; margin-bottom:12px; }
.toc-box ol { list-style:none; padding:0; margin:0; }
.toc-box li { margin:6px 0; }
.toc-box a { color:#457b9d; text-decoration:none; font-size:14px; display:block; padding:4px 8px; border-radius:6px; }
.toc-box a:hover { background:#e8edf3; }
.section h2 { scroll-margin-top:80px; }
.key-insight { background:#fff8e1; border-left:4px solid #f4a261; padding:16px 20px; margin:16px 0; border-radius:0 8px 8px 0; }
.toc-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px 28px; margin:28px 0; }
.toc-box h3 { font-size:16px; color:#1e3a5f; margin-bottom:12px; }
.toc-box ol { list-style:none; padding:0; margin:0; }
.toc-box li { margin:6px 0; }
.toc-box a { color:#457b9d; text-decoration:none; font-size:14px; display:block; padding:4px 8px; border-radius:6px; }
.toc-box a:hover { background:#e8edf3; }
.section h2 { scroll-margin-top:80px; }

.article-layout { display: grid; grid-template-columns: 1fr 280px; gap: 36px; max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.article-main { min-width: 0; }
.article-main .container { max-width: 100%; padding: 0; }
.article-sidebar { position: sticky; top: 80px; align-self: start; }
.article-sidebar .sc { background: #fff; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 8px rgba(0,0,0,0.05); }
.article-sidebar .sc h4 { font-size: 14px; color: #1e3a5f; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 2px solid #e63946; }
.article-sidebar .sc ul { list-style: none; padding: 0; margin: 0; }
.article-sidebar .sc li { margin: 5px 0; }
.article-sidebar .sc a { color: #457b9d; text-decoration: none; font-size: 13px; display: block; padding: 4px 0; }
.article-sidebar .sc a:hover { color: #1e3a5f; }
.side-stat { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
.side-stat .num { font-weight: 700; color: #1e3a5f; }
.side-stat .lbl { color: #666; }
.side-meta { font-size: 12px; color: #999; line-height: 1.6; }
@media (max-width: 900px) { .article-layout { grid-template-columns: 1fr; } .article-sidebar { position: static; } }
</style>"""

COOKIE_JS = """
<div id="cookie-banner">
  <div style="max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <span>本網站使用 Cookie 來改善您的瀏覽體驗及顯示個人化廣告。繼續使用即表示您同意 <a href="/privacy">私隱政策</a>。</span>
    <button onclick="document.getElementById('cookie-banner').style.display='none';localStorage.setItem('cookie_consent','true')" style="background:#f4a261;border:none;color:#1a2332;padding:10px 24px;border-radius:8px;font-weight:600;cursor:pointer;white-space:nowrap;">我了解</button>
  </div>
</div>
<script>
if(!localStorage.getItem('cookie_consent')){document.getElementById('cookie-banner').style.display='block'}
</script>"""

def build_head(title, desc, keywords, og_image, full_url, json_ld_str, is_home=False, extra_meta=""):
    site_name = SITE["name"]
    og_type = "website" if is_home else "article"
    google_verify = SEO.get("googleSiteVerification", "")
    verify_meta = ""
    if google_verify:
        verify_meta = f'<meta name="google-site-verification" content="{google_verify}">'
    parts = [
        '<!DOCTYPE html>',
        f'<html lang="{SITE["lang"]}">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{title}</title>',
        f'<meta name="description" content="{desc}">',
        f'<meta name="keywords" content="{keywords}">',
        verify_meta,
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:image" content="{og_image}">',
        f'<meta property="og:url" content="{full_url}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{site_name}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<link rel="canonical" href="{full_url}">',
        f'<script type="application/ld+json">{json_ld_str}</script>',
        extra_meta,
        '<script src="https://cdn.tailwindcss.com"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>',
        HEADER_CSS,
        '</head>'
    ]
    return "\n".join(p for p in parts if p)

def build_nav(current_url="/"):
    items = []
    for item in NAV:
        active = ' class="active"' if item["href"] == current_url else ""
        items.append(f'<li><a href="{item["href"]}"{active}>{item["label"]}</a></li>')
    return "\n".join(items)

def build_header(nav_html):
    return f'''<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-logo">HK<span>Info</span> 香港資訊數據圖鑑</a>
    <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
    <ul class="nav-links">{nav_html}</ul>
  </div>
</header>'''

def build_footer():
    ftr = SITE["footer"]
    nav_links = "".join(f'<li><a href="{item["href"]}">{item["label"]}</a></li>' for item in NAV)
    return f'''<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-grid">
      <div><h4>{SITE["name"]}</h4><p>{ftr["about"]}</p></div>
      <div><h4>快速連結</h4><ul>{nav_links}</ul></div>
      <div><h4>免責聲明</h4><p>{ftr["disclaimer"]}</p></div>
    </div>
    <div class="footer-bottom">
      <p>{ftr["copyright"]}</p>
      <p>數據來源：政府統計處、差餉物業估價署、房屋委員會及相關政府部門</p>
    </div>
  </div>
</footer>'''

def wrap_html(title, desc, keywords, og_image, url, json_ld, body_content, is_home=False):
    base_url = SITE["baseUrl"].rstrip("/")
    full_url = base_url + url
    jld = json.dumps(json_ld, ensure_ascii=False) if isinstance(json_ld, dict) else str(json_ld)
    head = build_head(title, desc, keywords, og_image, full_url, jld, is_home)
    nav = build_nav(url)
    header = build_header(nav)
    footer = build_footer()
    return "\n".join([
        head,
        '<body>',
        header,
        body_content,
        footer,
        COOKIE_JS,
        '</body>',
        '</html>'
    ])

def build_article_page(article):
    slug = article["slug"]
    title = article["title"]
    seo_data = article["seo"]
    
    hero_img = SITE["baseUrl"].rstrip("/") + '/images/' + article.get("heroImage", "placeholder-cityscape-1") + '.svg'
    
    hero_parts = [
        '<div class="hero">',
        f'  <h1>{title}</h1>',
        f'  <p>{article["summary"][:200]}...</p>',
        f'  <img src="{hero_img}" alt="{title}" class="hero-img" onerror="this.style.display=\'none\'">',
        f'  <p class="hero-caption">{article.get("heroCaption","")}</p>',
        '</div>'
    ]
    hero_html = "\n".join(hero_parts)
    
    breadcrumb = f'<div class="breadcrumb" style="max-width:1200px;margin:0 auto;padding:0 24px;"><a href="/">首頁</a> › <span>{title}</span></div>'
    
    # Generate table of contents
    toc_items = ""
    for ti, tsec in enumerate(article["sections"]):
        short_title = tsec["heading"][:45]
        if len(tsec["heading"]) > 45: short_title += "..."
        toc_items += '<li><a href="#sec-' + str(ti) + '">' + short_title + '</a></li>' + "\n"
    toc_html = '<div class="container"><div class="toc-box"><h3>' + chr(30446) + chr(24465) + '</h3><ol>' + toc_items + '</ol></div></div>'

    sections_html = ""
    charts_js = "window.__charts = window.__charts || {};\n"
    interleaved_charts = set()
    for idx, sec in enumerate(article["sections"]):
        sections_html += f'<div class="section container"><h2 id="sec-{idx}">{sec["heading"]}</h2>{sec["content"]}</div>\n'
    
    summary = f'<div class="container"><div class="summary-box"><h3>重點摘要</h3><p>{article["summary"]}</p></div></div>'
    meta = f'<div class="container"><div class="meta-info"><span>最後更新：{article.get("lastUpdated","")}</span><span>數據來源：<a href="{article.get("dataSourceUrl","#")}" target="_blank" rel="noopener">{article.get("dataSource","")}</a></span></div></div>'
    
    charts_js = "window.__charts = window.__charts || {};\n"
    charts_html = ""
    for ch in article.get("charts", []):
        cid = ch["id"]
        opt = json.dumps(ch["option"], ensure_ascii=False)
        charts_js += f"window.__charts['{cid}'] = {opt};\n"
        charts_html += f'<div class="container"><div class="chart-box"><h3>{ch["title"]}</h3><div id="{cid}" data-chart-id="{cid}" style="width:100%;height:{ch.get("height",400)}px"></div></div></div>\n'
    
    tables_html = ""
    for key, tbl in article.get("dataTables", {}).items():
        headers = "".join(f"<th>{h}</th>" for h in tbl["headers"])
        rows = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in tbl["rows"])
        tables_html += f'<div class="container"><div class="section"><h2>{tbl["title"]}</h2><div style="overflow-x:auto"><table class="data-table"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div></div></div>\n'
    
    related_parts = []
    for rel_slug in article.get("relatedArticles", []):
        rel = load_article(rel_slug)
        if rel:
            related_parts.append(f'<a href="/{rel["slug"]}" class="related-card"><h4>{rel["title"][:50]}...</h4><p>{rel["summary"][:120]}...</p><span style="color:#457b9d;font-size:13px;">閱讀更多 →</span></a>')
    related_section = f'<div class="section container"><h2>相關分析</h2><div class="grid-2">{"".join(related_parts)}</div></div>' if related_parts else ""
    
        # Sidebar HTML
    sidebar_parts = []
    # TOC
    toc_items = ""
    for si, sec in enumerate(article.get("sections", [])):
        sh = sec["heading"][:28]
        if len(sec["heading"]) > 28: sh += "..."
        toc_items += f"<li><a href=\"#sec-{si}\">{sh}</a></li>"
    if toc_items:
        sidebar_parts.append(f"<div class=\"sc\"><h4>本篇導讀</h4><ul>{toc_items}</ul></div>")
    # Stats from data tables
    for key, tbl in article.get("dataTables", {}).items():
        rows = tbl.get("rows", [])
        if rows and len(rows) > 0:
            stats = "".join(f"<div class=\"side-stat\"><span class=\"lbl\">{r[0]}</span><span class=\"num\">{r[1]}</span></div>" for r in rows[-4:])
            sidebar_parts.append(f"<div class=\"sc\"><h4>重點數據</h4>{stats}</div>")
        break
    # Related
    rel_items = ""
    for rs in article.get("relatedArticles", []):
        try:
            rp = os.path.join(os.path.dirname(__file__), "src", "articles", rs + ".json")
            with open(rp, "r", encoding="utf-8") as rf:
                ra = json.load(rf)
            rel_items += f"<li><a href=\"/{rs}\">{ra.get('title','?')[:35]}</a></li>"
        except:
            pass
    if rel_items:
        sidebar_parts.append(f"<div class=\"sc\"><h4>相關分析</h4><ul>{rel_items}</ul></div>")
    # Meta
    lu = article.get("lastUpdated", "")
    ds = article.get("dataSource", "")
    meta_side = f"<div class=\"sc\"><h4>資訊標籤</h4><div class=\"side-meta\"><p>最後更新: {lu}</p><p>數據來源: {ds}</p></div></div>"
    sidebar_parts.append(meta_side)
    sidebar_html = "".join(sidebar_parts)
    
    main_content = "\n".join([summary, meta, sections_html, charts_html, tables_html])
    body_content = "\n".join([hero_html, breadcrumb, "<div class=\"article-layout\"><div class=\"article-main\">", main_content, "</div><div class=\"article-sidebar\">", sidebar_html, "</div></div>", related_section])
    body_content += f'\n<script>{charts_js}</script>\n'
    body_content += '''
<script>
document.addEventListener('DOMContentLoaded',function(){
    var charts=document.querySelectorAll('[data-chart-id]');
    charts.forEach(function(el){
        var id=el.getAttribute('data-chart-id');
        if(window.__charts&&window.__charts[id]){var chart=echarts.init(el);chart.setOption(window.__charts[id]);window.addEventListener('resize',function(){chart.resize();})}
    });
});
</script>'''
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": seo_data["description"],
        "dateModified": article.get("lastUpdated", ""),
        "author": {"@type": "Person", "name": AUTHOR["name"]},
        "publisher": {"@type": "Organization", "name": SITE["name"]},
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE["baseUrl"].rstrip("/") + "/" + slug}
    }
    
    return wrap_html(
        seo_data["title"], seo_data["description"], seo_data["keywords"],
        hero_img, "/" + slug, json_ld, body_content
    )

def build_page(article):
    """For simple content pages like Privacy, About (no charts, no hero image)"""
    slug = article["slug"]
    title = article["title"]
    seo_data = article["seo"]
    
    hero_img = SITE["baseUrl"].rstrip("/") + "/images/og-default.svg"
    
    hero_html = f'<div class="page-hero"><h1>{title}</h1></div>'
    breadcrumb = f'<div class="breadcrumb" style="max-width:1200px;margin:0 auto;padding:0 24px;"><a href="/">首頁</a> › <span>{title}</span></div>'
    
    content_html = f'<div class="container"><div class="plain-content">'
    for sec in article["sections"]:
        content_html += f'<h2>{sec["heading"]}</h2>{sec["content"]}\n'
    content_html += f'</div></div>'
    
    body_content = "\n".join([hero_html, breadcrumb, content_html])
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": seo_data["description"],
        "author": {"@type": "Person", "name": AUTHOR["name"]},
        "publisher": {"@type": "Organization", "name": SITE["name"]}
    }
    
    return wrap_html(
        seo_data["title"], seo_data["description"], seo_data["keywords"],
        hero_img, "/" + slug, json_ld, body_content
    )

def build_index_page(articles):
    hero_parts = [
        '<div class="index-hero">',
        f'  <h1>{SITE["name"]}</h1>',
        f'  <p>{SITE["tagline"]}</p>',
        '  <div style="margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">',
        '    <span class="tag" style="background:rgba(255,255,255,0.15);color:#fff;">📈 樓價分析</span>',
        '    <span class="tag" style="background:rgba(255,255,255,0.15);color:#fff;">🏠 公屋輪候</span>',
        '    <span class="tag" style="background:rgba(255,255,255,0.15);color:#fff;">💰 收入分析</span>',
        '    <span class="tag" style="background:rgba(255,255,255,0.15);color:#fff;">🏢 空置率</span>',
        '    <span class="tag" style="background:rgba(255,255,255,0.15);color:#fff;">🗺️ 18區數據</span>',
        '  </div>',
        '</div>'
    ]
    hero_html = "\n".join(hero_parts)
    
    stats = [
        '<div class="container" style="margin-top:-30px;position:relative;z-index:10;">',
        '  <div class="grid-3">',
        '    <div class="stat-bar"><div class="num">5</div><div class="label">分析指標</div></div>',
        '    <div class="stat-bar"><div class="num">18區</div><div class="label">全港覆蓋</div></div>',
        '    <div class="stat-bar"><div class="num">2015-2025</div><div class="label">十年數據</div></div>',
        '  </div>',
        '</div>'
    ]
    stats_html = "\n".join(stats)
    
    cards = []
    for art in articles:
        img = f'/images/{art.get("heroImage","og-default")}.svg'
        kw = "".join(f'<span class="tag">{k.strip()}</span>' for k in art["seo"]["keywords"].split(",")[:3])
        cards.append(f'<a href="/{art["slug"]}" class="home-card">')
        cards.append(f'  <img src="{img}" alt="{art["title"]}" class="home-card-img" onerror="this.style.display=\'none\'" style="background:#1e3a5f;height:180px;">')
        cards.append(f'  <div class="home-card-body">')
        cards.append(f'    <h3>{art["title"]}</h3>')
        cards.append(f'    <p>{art["summary"][:200]}...</p>')
        cards.append(f'    <div class="tags">{kw}</div>')
        cards.append(f'  </div>')
        cards.append(f'</a>')
    
    cards_grid = f'<div class="section container"><h2>分析指標</h2><div class="grid-2">{"".join(cards)}</div></div>'
    
    about = [
        '<div class="section container">',
        f'  <h2>關於 {SITE["shortName"]}</h2>',
        f'  <p>{SITE["description"]}</p>',
        '  <p>我們的主要數據來源包括：</p>',
        '  <ul style="margin:12px 0 0 20px;line-height:2;">',
        '    <li>差餉物業估價署（RVD）— 物業市場統計</li>',
        '    <li>政府統計處（C&SD）— 綜合住戶統計、人口普查</li>',
        '    <li>房屋委員會 — 公屋輪候及供應數據</li>',
        '    <li>其他政府部門公開數據</li>',
        '  </ul>',
        '</div>'
    ]
    about_html = "\n".join(about)
    
    body_content = "\n".join([hero_html, stats_html, cards_grid, about_html])
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["name"],
        "description": SITE["description"],
        "url": SITE["baseUrl"],
        "author": {"@type": "Person", "name": AUTHOR["name"]}
    }
    
    return wrap_html(
        SEO["defaultTitle"], SEO["defaultDescription"], SEO["defaultKeywords"],
        SITE["baseUrl"].rstrip("/") + "/images/og-default.svg",
        "/", json_ld, body_content, is_home=True
    )

def load_article(slug):
    try:
        return load_json(f"articles/{slug}.json")
    except:
        return None

def build_sitemap(articles, pages):
    base = SITE["baseUrl"].rstrip("/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    lines.append(f'  <url><loc>{base}/</loc><priority>1.0</priority><changefreq>weekly</changefreq></url>')
    for art in articles:
        lines.append(f'  <url><loc>{base}/{art["slug"]}</loc><priority>0.9</priority><changefreq>monthly</changefreq><lastmod>{art.get("lastUpdated","")}</lastmod></url>')
    for p in pages:
        lines.append(f'  <url><loc>{base}/{p["slug"]}</loc><priority>0.6</priority><changefreq>monthly</changefreq><lastmod>{p.get("lastUpdated","")}</lastmod></url>')
    lines.append('</urlset>')
    return "\n".join(lines)

def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True)
    
    article_slugs = ["rental-price-index", "public-housing", "income-vs-price", "vacancy-rate", "homeownership-district", "birth-death-rate", "marriage-divorce", "life-expectancy", "foreign-domestic-helpers", "net-migration", "retail-sales", "tourist-arrivals", "ecommerce-rate", "restaurant-turnover", "consumer-price-index", "salary-median", "unemployment-age", "student-numbers", "graduate-employment", "work-hours", "museum-attendance", "library-borrowing", "public-transport", "private-car-ev", "traffic-accidents", "top-diseases", "hospital-bed-occupancy", "hot-days", "solid-waste", "air-quality"]
    articles = []
    for slug in article_slugs:
        art = load_article(slug)
        if art:
            articles.append(art)
            print(f"  Loaded: {art['title']}")
    
    page_slugs = ["privacy", "about"]
    pages = []
    for slug in page_slugs:
        p = load_article(slug)
        if p:
            pages.append(p)
            print(f"  Loaded page: {p['title']}")
    
    print("Generating index...")
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(build_index_page(articles))
    
    for art in articles:
        name = art["title"][:40]
        print(f"Generating article: {name}...")
        with open(OUTPUT_DIR / f"{art['slug']}.html", "w", encoding="utf-8") as f:
            f.write(build_article_page(art))
    
    for p in pages:
        name = p["title"][:40]
        print(f"Generating page: {name}...")
        with open(OUTPUT_DIR / f"{p['slug']}.html", "w", encoding="utf-8") as f:
            f.write(build_page(p))
    
    sitemap = build_sitemap(articles, pages)
    with open(OUTPUT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    
    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE['baseUrl'].rstrip('/')}/sitemap.xml\n"
    with open(OUTPUT_DIR / "robots.txt", "w", encoding="utf-8") as f:
        f.write(robots)
    
    # ads.txt for Google AdSense
    pid = ADSENSE.get("publisherId", "")
    if pid:
        ads = f"google.com, {pid}, DIRECT, f08c47fec0942fa0\n"
    else:
        ads = "# Please set adsense.publisherId in src/data/config.json"
    with open(OUTPUT_DIR / "ads.txt", "w", encoding="utf-8") as f:
        f.write(ads)
    
    img_src = SRC_DIR / "images"
    img_dst = OUTPUT_DIR / "images"
    if img_src.exists():
        shutil.copytree(img_src, img_dst)
        print(f"  Copied {len(list(img_src.glob('*')))} images")
    
    total = 2 + len(articles) + len(pages)
    print(f"\nDone! Generated {total} files to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()