#!/usr/bin/env python3
"""Rebuild the pages, run the checker, then zip the website for cPanel upload.

Usage: python3 tools/package.py
Writes dist/ncf-site-preview.zip (or dist/ncf-site-live.zip when build_pages.PREVIEW is False).
Refuses to package if the checker fails.
"""
import os
import re
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_pages  # noqa: E402
from check_site import check  # noqa: E402

SITE = ROOT
# only these go in the cPanel zip; tools, docs and git files stay out
WEB = ("assets", "images", "media")

build_pages.build()
fails, n = check(SITE)
if build_pages.PREVIEW:
    # the checker requires noindex; that's right for the preview build
    pass
else:
    # live build: noindex is gone on purpose, and no Joy markers may remain
    fails = [f for f in fails if "noindex" not in f]
    for name in os.listdir(SITE):
        if not name.endswith(".html"):
            continue
        text = open(os.path.join(SITE, name), encoding="utf-8").read()
        if re.search(r'Joy to confirm|class="confirm"|class="[^"]*\bdraft\b', text):
            fails.append(f"{name}: still has [Joy to confirm] markers or a draft frame")
if fails:
    print("Not packaged. Fix these first:")
    for f in fails:
        print("  -", f)
    sys.exit(1)

name = "ncf-site-preview.zip" if build_pages.PREVIEW else "ncf-site-live.zip"
os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
out = os.path.join(ROOT, "dist", name)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") or f == ".htaccess":
            z.write(os.path.join(SITE, f), f)
    for top in WEB:
        for dirpath, _, files in os.walk(os.path.join(SITE, top)):
            for f in files:
                if f.startswith("."):
                    continue
                full = os.path.join(dirpath, f)
                z.write(full, os.path.relpath(full, SITE))
print(f"OK {n} checks · wrote dist/{name} ({os.path.getsize(out) // 1024} KB)")
