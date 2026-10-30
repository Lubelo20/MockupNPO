# NCF website: handover

Six static pages: Home, Our Story, Programmes, Impact, Get Involved, Contact.
There's no database and no build server. cPanel just serves the files.

## Folders

| Path | What it is |
|---|---|
| `tools/pages/*.html` | **Edit these.** The page content, without header and footer. |
| `tools/build_pages.py` | Adds the shared header, footer and SEO tags, and writes the pages at the repo root. Has the `PREVIEW` and `SITE_URL` switches. |
| `*.html`, `assets/`, `images/`, `media/` (repo root) | The finished website. This is what goes on cPanel. Don't edit the `.html` files by hand, because they get overwritten; the CSS and JS in `assets/` are edited directly. |
| `tools/check_site.py` | Checks links, images, quotes, the WhatsApp number and hidden impact slots. |
| `tools/package.py` | Rebuilds, checks, and zips the website into `dist/`. |
| `index.html`, `images/` (project root) | The old one-page site, kept untouched for reference. |

After any edit, run `python3 tools/package.py`.

## 1. Private preview for Joy

1. Run `python3 tools/package.py` to get `dist/ncf-site-preview.zip`.
2. cPanel → **File Manager** → `public_html` → create a folder `preview`.
3. Upload the zip into `preview`, then right-click → **Extract**. Delete the zip afterwards.
4. cPanel → **Directory Privacy** → `public_html/preview` → tick *Password protect*, then create a user and password for Joy.
5. Send Joy the link (`https://<domain>/preview/`) and the login.

The preview pages already tell search engines not to index them.

## 2. What Joy needs to check

The highlighted yellow boxes are the parts only Joy can write:

```
grep -n "Joy to confirm" tools/pages/*.html
```

- `index.html`: none. "Why we exist" is written in the foundation's voice from known facts (Nkululeko = freedom), so Joy only needs to read it.
- `about.html`: none left. The founder section now uses only the real bio and credentials from the original site.

Paragraphs written in Joy's voice sit inside a dashed yellow frame labelled *"Drafted in Joy's voice"* (`<div class="draft" …>` in `about.html`). Joy rewrites or approves every sentence in those frames.

To finish: replace each `<mark class="confirm">[…]</mark>` with Joy's own words, then remove the `draft` frame (keep the paragraphs, delete the `<div class="draft" …>` wrapper, or on the home page change `class="body draft"` to `class="body"`). The live package refuses to build while any marker or frame is left.

## 3. Impact numbers

In `tools/pages/impact.html`, find `IMPACT FIGURES`. For each slot (parcels, boxes, learners, items) that Joy has a real number for:

```html
<div class="figure" data-figure="boxes" data-value="120"><b>120</b><span>Comfort boxes given to students</span></div>
```

Put the number in **both** `data-value` and `<b>`, and delete `hidden`. Leave the slots without a confirmed number hidden.

## 4. Going live

1. All markers are replaced, and Joy has approved the preview.
2. In `tools/build_pages.py`, set `PREVIEW = False` and `SITE_URL = "https://<your-domain>"`.
3. Run `python3 tools/package.py` to get `dist/ncf-site-live.zip`. It refuses to package if any `[Joy to confirm]` markers are left.
4. cPanel → File Manager → `public_html`: back up and move the old `index.html` and `images/`, then upload and extract the live zip there.
5. Delete the `preview` folder and remove its Directory Privacy.
6. Open the site on a phone and send a test WhatsApp message from the Contact page.
