#!/usr/bin/env python3
"""Wrap each page body in tools/pages/ with the shared head, header and footer.

Usage: python3 tools/build_pages.py   (writes the *.html pages at the repo root)
The output is plain static HTML; nothing here runs on the server.
Set PREVIEW = False before the public launch to drop the noindex tag.
"""
import hashlib
import json
import os
import re

PREVIEW = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "pages")
OUT = ROOT  # the site lives at the repo root so GitHub Pages serves index.html
SITE_URL = ""  # e.g. "https://www.ncf.org.za" once the domain is known

NAV = [("index.html", "Home"), ("about.html", "Our Story"), ("programmes.html", "Programmes"),
       ("impact.html", "Impact"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]

HEAD = """<!doctype html>
<html lang="en" class="no-js" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<meta name="theme-color" content="#FFFFFF">
<meta name="color-scheme" content="light">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nonkululeko Catherine Foundation">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_image}">
<link rel="icon" href="images/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={v_css}">
<script>document.documentElement.classList.replace('no-js','js')</script>
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap nav">
    <a class="brand brand-logo" href="index.html" aria-label="Nonkululeko Catherine Foundation, home"><picture><source type="image/webp" srcset="images/logo.webp"><img src="images/logo.jpg" alt="Nonkululeko Catherine Foundation logo" width="56" height="56"></picture></a>
    <nav class="links" id="links" aria-label="Main">
{nav}
      <a class="btn" href="get-involved.html">Get involved <span class="arr">→</span></a>
    </nav>
    <button id="menu-btn" type="button" aria-expanded="false" aria-controls="links" aria-label="Open menu"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer>
  <div class="wrap">
    <div class="f-top">
      <div class="f-about">
        <a class="brand" href="index.html"><picture><source type="image/webp" srcset="images/logo.webp"><img src="images/logo.jpg" alt="Nonkululeko Catherine Foundation logo" width="44" height="44" loading="lazy" decoding="async"></picture><span><b>Nonkululeko Catherine Foundation</b><small>We care beyond measure</small></span></a>
        <p>A registered non-profit in KwaZulu-Natal, empowering teenagers and communities through education, essential resources and care.</p>
        <div class="social">
          <a href="https://www.instagram.com/official_ncf/" target="_blank" rel="noopener" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
          <a href="https://wa.me/27815161673" target="_blank" rel="noopener" aria-label="WhatsApp"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19l-4 1Z"/></svg></a>
          <a href="mailto:thenonkululekofoundation@gmail.com" aria-label="Email"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg></a>
        </div>
      </div>
      <div><h4>Foundation</h4><ul><li><a href="about.html">Our story</a></li><li><a href="about.html#founder">Leadership</a></li><li><a href="impact.html">Impact</a></li><li><a href="gallery.html">Gallery</a></li></ul></div>
      <div><h4>Programmes</h4><ul><li><a href="programmes.html#outreach">School outreach</a></li><li><a href="programmes.html#parcels">Food parcels</a></li><li><a href="programmes.html#clothing">Clothing Drive</a></li><li><a href="programmes.html#dignity">Comfort &amp; Dignity</a></li></ul></div>
      <div><h4>Connect</h4><ul><li><a href="get-involved.html">Get involved</a></li><li><a href="get-involved.html#partner">Partner with us</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    </div>
    <div class="f-bot"><span>© <span id="yr">2026</span> The Nonkululeko Catherine Foundation · Website by Lubelo Tech Solutions</span><a href="#main">Back to top ↑</a></div>
  </div>
</footer>
<script src="assets/js/site.js?v={v_js}"></script>
</body>
</html>
"""

NGO = {
    "@context": "https://schema.org",
    "@type": "NGO",
    "name": "The Nonkululeko Catherine Foundation",
    "alternateName": "NCF",
    "slogan": "We care beyond measure",
    "description": "A registered non-profit in KwaZulu-Natal empowering teenagers and communities through education, essential resources and care.",
    "foundingDate": "2022",
    "email": "thenonkululekofoundation@gmail.com",
    "telephone": "+27815161673",
    "areaServed": "KwaZulu-Natal, South Africa",
    "founder": {"@type": "Person", "name": "Sinalenjabulo Joy Ndlovu"},
    "sameAs": ["https://www.instagram.com/official_ncf/"],
}


IMG_TAG = re.compile(r"<img\b[^>]*>")


def webp_of(path):
    """images/x.jpg -> images/x.webp when that file exists, else None."""
    w = re.sub(r"\.jpe?g$", ".webp", path)
    return w if w != path and os.path.exists(os.path.join(OUT, w)) else None


def optimise_images(html):
    """Serve WebP with the JPEG as fallback, lazy-load everything but the hero,
    and return a preload tag for the hero so the browser fetches it first."""
    preload = ""
    out, pos = [], 0
    for m in IMG_TAG.finditer(html):
        tag = m.group(0)
        if "data-plain" in tag:  # the gallery viewer swaps this src in JS; a <picture> would override it
            out.append(html[pos:m.start()] + tag)
            pos = m.end()
            continue
        hero = 'class="hero-bg"' in tag
        if "decoding=" not in tag:
            tag = tag[:-1] + ' decoding="async">'
        if not hero and "loading=" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        inside_picture = html.rfind("<picture", 0, m.start()) > html.rfind("</picture>", 0, m.start())
        src = re.search(r'src="([^"]+)"', tag).group(1)
        srcset = re.search(r'srcset="([^"]+)"', tag)
        sizes = re.search(r'sizes="([^"]+)"', tag)
        if srcset:
            parts = [s.strip().split() for s in srcset.group(1).split(",")]
            webps = [webp_of(u) for u, _ in parts]
            wset = ", ".join(f"{w} {d}" for w, (_, d) in zip(webps, parts)) if all(webps) else ""
        else:
            w = webp_of(src)
            wset = w or ""
        if hero and wset and not inside_picture:
            preload = (f'<link rel="preload" as="image" type="image/webp" imagesrcset="{wset}"'
                       + (f' imagesizes="{sizes.group(1)}"' if sizes else "") + ' fetchpriority="high">\n')
        if wset and not inside_picture:
            tag = (f'<picture><source type="image/webp" srcset="{wset}"'
                   + (f' sizes="{sizes.group(1)}"' if sizes else "") + f'>{tag}</picture>')
        out.append(html[pos:m.start()] + tag)
        pos = m.end()
    out.append(html[pos:])
    html = "".join(out)
    html = re.sub(r'poster="(media/[^"]+)\.jpg"',
                  lambda m: f'poster="{m.group(1)}.webp"' if os.path.exists(os.path.join(OUT, m.group(1) + ".webp")) else m.group(0),
                  html)
    return html, preload


def ver(rel):
    """Short content hash so browsers fetch the new file after every change."""
    data = open(os.path.join(OUT, "assets", rel), "rb").read()
    return hashlib.md5(data).hexdigest()[:8]


def build():
    for fname in sorted(os.listdir(SRC)):
        if not fname.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, fname), encoding="utf-8").read()
        # front matter: <!-- title: ... --> and <!-- desc: ... -->
        meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", raw.split("\n\n", 1)[0]))
        body = raw.split("\n\n", 1)[1]
        nav = "\n".join(f'      <a href="{h}">{t}</a>' for h, t in NAV)
        extra = ""
        if fname == "index.html":
            ngo = dict(NGO)
            if SITE_URL:
                ngo["url"] = SITE_URL
                ngo["logo"] = SITE_URL + "/images/logo.jpg"
            extra = '<script type="application/ld+json">' + json.dumps(ngo) + "</script>\n"
        body, preload = optimise_images(body)
        extra = preload + extra
        og_image = (SITE_URL + "/" if SITE_URL else "") + "images/founder.jpg"
        html = HEAD.format(
            title=meta["title"], desc=meta["desc"], nav=nav, extra_head=extra, og_image=og_image,
            robots='<meta name="robots" content="noindex, nofollow">\n' if PREVIEW else "",
            v_css=ver("css/site.css"),
        ) + body.rstrip() + "\n" + FOOT.replace("{v_js}", ver("js/site.js"))
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)
        print("wrote " + fname)


if __name__ == "__main__":
    build()
