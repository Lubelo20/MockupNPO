# Nonkululeko Catherine Foundation website (mockup)

A seven-page static website for the Nonkululeko Catherine Foundation, a registered NPO in KwaZulu-Natal.
Built by Lubelo Tech Solutions.

- The finished website sits at the repo root: the seven `*.html` pages plus `assets/`, `images/` and `media/`. GitHub Pages serves it straight from `main`.
- `tools/pages/` holds each page's body; `tools/build_pages.py` wraps them with the shared header and footer.
- `tools/check_site.py` checks links, images, titles and the contact form.
- `tools/package.py` rebuilds, checks and zips the website (pages, `assets/`, `images/`, `media/`) for cPanel upload.

```
python3 tools/package.py
```

This is a preview build: every page carries `noindex`, so search engines won't list it.
See `HANDOVER.md` for the cPanel upload and go-live steps.
