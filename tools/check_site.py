#!/usr/bin/env python3
"""Check the NCF static site against the spec's rules.

Usage: python3 tools/check_site.py [site_dir]   (defaults to the repo root)
Exits 0 and prints "OK n checks", or exits 1 and lists the failures.
"""
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs

PAGES = ["index.html", "about.html", "programmes.html", "impact.html",
         "get-involved.html", "contact.html", "gallery.html"]
FOUNDER_QUOTE = ("The idea and the vision became a reality. "
                 "Then the hard work began, and a foundation was laid.")
WA_NUMBER = "27815161673"
MAX_IMG_WIDTH = 1200
MAX_HERO_WIDTH = 2000  # full-screen hero backgrounds (images/hero-*.jpg)


class Page(HTMLParser):
    """Collects the bits of a page the checks need."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.metas = []
        self.links = []        # (tag, attr, value)
        self.imgs = []         # attrs dict
        self.figures = []      # attrs dict of [data-figure]
        self.options = {}      # select id -> [option values]
        self.forms = []
        self.ids = set()
        self.quotes = []       # text inside blockquote / .quote
        self.footer_text = ""
        self.has_menu_btn = False
        self._stack = []
        self._in_title = False
        self._select = None
        self._quote_depth = 0
        self._quote_buf = ""
        self._footer_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in ("img", "meta", "link", "br", "input", "source", "hr"):
            self._stack.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            self.metas.append(a)
        for attr in ("href", "src"):
            if attr in a and tag != "meta":
                self.links.append((tag, attr, a[attr]))
        if tag == "img":
            self.imgs.append(a)
        if "data-figure" in a:
            self.figures.append(a)
        if tag == "select":
            self._select = a.get("id", "")
            self.options[self._select] = []
        if tag == "option" and self._select is not None:
            self.options[self._select].append(a.get("value", ""))
        if tag == "form":
            self.forms.append(a)
        if a.get("id") == "menu-btn" and a.get("aria-controls") == "links":
            self.has_menu_btn = True
        classes = (a.get("class") or "").split()
        if self._quote_depth:
            self._quote_depth += 1
        elif tag == "blockquote" or "quote" in classes:
            self._quote_depth = 1
            self._quote_buf = ""
        if self._footer_depth:
            self._footer_depth += 1
        elif tag == "footer":
            self._footer_depth = 1

    def handle_endtag(self, tag):
        if self._stack:
            self._stack.pop()
        if tag == "title":
            self._in_title = False
        if tag == "select":
            self._select = None
        if self._quote_depth:
            self._quote_depth -= 1
            if not self._quote_depth:
                self.quotes.append(" ".join(self._quote_buf.split()))
        if self._footer_depth:
            self._footer_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._quote_depth:
            self._quote_buf += data
        if self._footer_depth:
            self.footer_text += data


def is_local(url):
    return not re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", url)


def image_width(path):
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", path],
                             capture_output=True, text=True).stdout
        m = re.search(r"pixelWidth: (\d+)", out)
        return int(m.group(1)) if m else 0
    except FileNotFoundError:
        return 0


def check(site):
    fails, n = [], 0

    def ok(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            fails.append(msg)

    parsed = {}
    for name in PAGES:
        path = os.path.join(site, name)
        ok(os.path.isfile(path), f"{name}: missing")
        if not os.path.isfile(path):
            continue
        p = Page()
        p.feed(open(path, encoding="utf-8").read())
        parsed[name] = p

        ok(p.title.strip(), f"{name}: empty <title>")
        ok(any(m.get("name") == "description" and m.get("content") for m in p.metas),
           f"{name}: no meta description")
        ok(any(m.get("name") == "robots" and "noindex" in m.get("content", "") for m in p.metas),
           f"{name}: no robots noindex (preview build)")
        hrefs = {urlparse(v).path for t, at, v in p.links if t == "a"}
        for target in PAGES:
            ok(target in hrefs, f"{name}: nav has no link to {target}")
        ok(p.has_menu_btn, f"{name}: no #menu-btn[aria-controls=links]")
        ok("Lubelo Tech Solutions" in p.footer_text, f"{name}: footer credit missing")

        for tag, attr, url in p.links:
            if not is_local(url) or not url:
                continue
            target = urlparse(url).path
            if target:
                ok(os.path.exists(os.path.join(site, target)),
                   f"{name}: broken {attr} {url}")
            frag = urlparse(url).fragment
            if frag and target in PAGES and target != name:
                pass  # checked after all pages are parsed

        for img in p.imgs:
            src = img.get("src", "?")
            ok(img.get("alt", "").strip(), f"{name}: img {src} has no alt")
            ok(img.get("width") and img.get("height"), f"{name}: img {src} no width/height")

        for q in p.quotes:
            ok(q.strip("“”\" ") == FOUNDER_QUOTE,
               f"{name}: quote not allowed (only the founder quote): {q[:60]!r}")

        for fig in p.figures:
            if not fig.get("data-value", "").strip():
                ok("hidden" in fig, f"{name}: empty figure {fig.get('data-figure')} not hidden")

    # cross-page: fragments, topics, WhatsApp form
    for name, p in parsed.items():
        for tag, attr, url in p.links:
            u = urlparse(url)
            if not is_local(url) or not u.path or u.path not in parsed:
                continue
            if u.fragment:
                ok(u.fragment in parsed[u.path].ids, f"{name}: missing anchor {url}")
            topic = parse_qs(u.query).get("topic")
            if topic and "contact.html" in parsed:
                ok(topic[0] in parsed["contact.html"].options.get("topic", []),
                   f"{name}: topic={topic[0]} has no matching option on contact.html")
    if "contact.html" in parsed:
        forms = parsed["contact.html"].forms
        ok(any(f.get("data-wa") == WA_NUMBER for f in forms),
           f"contact.html: no form[data-wa={WA_NUMBER}]")

    titles = [p.title.strip() for p in parsed.values()]
    ok(len(titles) == len(set(titles)), "titles are not unique")

    img_dir = os.path.join(site, "images")
    if os.path.isdir(img_dir):
        for f in sorted(os.listdir(img_dir)):
            w = image_width(os.path.join(img_dir, f))
            cap = MAX_HERO_WIDTH if f.startswith("hero-") else MAX_IMG_WIDTH
            ok(w <= cap, f"images/{f}: {w}px wide (max {cap})")

    return fails, n


if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fails, n = check(site)
    if fails:
        print(f"FAIL {len(fails)} of {n} checks")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print(f"OK {n} checks")
