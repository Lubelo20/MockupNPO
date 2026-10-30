# NCF Multi-page Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the single-page NCF site as a six-page static site that opens on Joy's "why we exist" story, packaged for upload to a private cPanel preview.

**Architecture:** Plain HTML pages that share one stylesheet (`assets/css/site.css`) and one script (`assets/js/site.js`). The header and footer markup is copied into each page (no build step, since cPanel serves the files as they are). A dependency-free Python checker (`tools/check_site.py`) is the test suite. It parses every page and enforces the spec's rules.

**Tech Stack:** HTML5, CSS (custom properties, grid, `clamp`), vanilla JS, Google Fonts (Bricolage Grotesque, Instrument Serif, DM Sans, as in the current site). Python 3 standard library for checks and packaging (`html.parser`, `zipfile`). `sips` (macOS) for image resizing.

**Spec:** `docs/superpowers/specs/2026-10-30-ncf-multipage-site-design.md`

## Global Constraints

- Output lives in `site/`. The original `index.html` and `images/` at the project root stay untouched as the source of truth.
- Pages: `index.html`, `about.html`, `programmes.html`, `impact.html`, `get-involved.html`, `contact.html`. Nav labels: Home, Our Story, Programmes, Impact, Get Involved, Contact.
- Brand tokens copied from the current `index.html` `:root` (including the dark-mode blocks), e.g. `--deep:#2A1640`, `--ink:#24123A`, `--magenta:#E4237C`, `--purple:#9B4DC8`, `--blue:#3E7CC4`, `--orange:#F08A2E`.
- No invented quotes, people or numbers. The only founder quote allowed is: "The idea and the vision became a reality. Then the hard work began, and a foundation was laid."
- Unknown story details use `<mark class="confirm">[Joy to confirm: …]</mark>`.
- Preview build: every page has `<meta name="robots" content="noindex">`.
- Contact: `081 516 1673`, WhatsApp `https://wa.me/27815161673`, `thenonkululekofoundation@gmail.com`, Instagram `@official_ncf` → `https://instagram.com/official_ncf`.
- No photo is rendered wider than its source width on desktop (sources are 163–776px). No full-bleed photo heroes.
- Footer on every page: "Website by Lubelo Tech Solutions".
- Phone-first: no horizontal scroll at 360px width, 16px+ side gutters.

## Review Focus

- Mobile menu: at phone width, tapping Menu opens the nav, and tapping a link or pressing Esc closes it (`aria-expanded` stays correct). The checker asserts that `#menu-btn` with `aria-controls="links"` is on every page, and Task 6 checks it by hand at 360px.
- Get Involved buttons link to `contact.html?topic=<key>`, and the contact form's select preselects that topic. An unknown or missing `?topic` falls back to the first option without errors. The checker asserts that every `topic=` value matches an `<option value>` on contact.html.
- WhatsApp message with an empty organisation field or apostrophes and emoji: the text is URL-encoded and there's no "Organisation: " line when it's empty. Task 3 includes a node-free manual check, plus the checker asserts that the form's `data-wa` equals `27815161673`.
- Broken internal links and images after moving into `site/`: the checker resolves every `href`/`src` that isn't http/mailto/tel/#.
- Impact figure slots left empty must not render as "0" or blank boxes. The checker asserts that every element with `data-figure` and an empty `data-value` has the `hidden` attribute.

---

### Task 1: Checker, shared assets, and image set

**Files:**
- Create: `tools/check_site.py`
- Create: `site/assets/css/site.css`, `site/assets/js/site.js`
- Create: `site/images/*` (copied from `images/`, then optimised)

**Interfaces:**
- Produces: `python3 tools/check_site.py [site_dir]` exits 0 and prints `OK n checks`, or exits 1 and lists the failures. Later tasks only add pages, and the checker already knows all six names.
- Produces CSS classes reused by every page: `.wrap`, `.eyebrow`, `.lede`, `.btn .btn-primary .btn-outline .btn-light`, `header .nav .brand .links #menu-btn`, `footer .f-top .f-bot`, `.card`, `.photo` (framed image, `max-width` set inline to the source width), `.letter` (founder letter block), `mark.confirm` (yellow-highlighted marker), `.figure[data-figure]`.
- Produces JS: marks the current nav link with `aria-current="page"`, toggles the mobile menu, reads `?topic=` into `#topic`, builds the WhatsApp URL from `form[data-wa]`, and sets the footer year.

- [ ] **Step 1: Write the checker.** For each of the six pages, it checks: the file exists; `<title>` is non-empty and unique; there's a meta description; there's a robots noindex meta; the nav has links to all six pages; `#menu-btn[aria-controls=links]`; the footer contains "Lubelo Tech Solutions"; every local `href`/`src` resolves inside `site/`; every `<img>` has non-empty `alt`, `width` and `height`; any `“…”` / `<blockquote>` / `.quote` text must equal the allowed founder quote; `data-figure` with empty `data-value` must be `hidden`; `topic=` values must exist as options on contact.html; `form[data-wa]` must be `27815161673`. If `site/images/` holds a file wider than 1200px, it fails.
- [ ] **Step 2: Run it.** `python3 tools/check_site.py site`. Expected: FAIL (the pages are missing).
- [ ] **Step 3: Copy the images** into `site/images/`. Re-encode the JPEGs at quality 80 with `sips -s formatOptions 80`, and don't upscale. Write `site.css` (tokens + dark mode copied from the current site; calmer spacing, `section{padding-block:clamp(64px,8vw,112px)}`) and `site.js`.
- [ ] **Step 4: Run it again.** Expected: it still FAILs, but only on missing pages.

### Task 2: Home page (story-first)

**Files:** Create `site/index.html`

**Interfaces:** Consumes the Task 1 classes. The header and footer markup written here is the canonical copy that Tasks 3–5 paste in unchanged.

- [ ] **Step 1: Build the sections in order.**
  (1) **Letter hero**: two columns on desktop, stacked on mobile. On the left, `founder.jpg` framed at max 606px with the caption "Sinalenjabulo Joy Ndlovu · Founder & Director". On the right, the eyebrow "Why we exist", an h1 like "From care *to change.*", a short drafted letter excerpt in Joy's voice using only spec facts, with one `mark.confirm` for who Nonkululeko Catherine is, the real founder quote, and a "Read Joy's story →" link to about.html.
  (2) The four-programme glimpse (cards → programmes.html#…).
  (3) A strip of 6 real photos with honest captions.
  (4) The six ways to help (→ get-involved.html#…).
  (5) A closing CTA band.
- [ ] **Step 2: Run the checker** for this page. Expected: index.html checks PASS.

### Task 3: Our Story + Contact pages

**Files:** Create `site/about.html`, `site/contact.html`

- [ ] **Step 1: Write about.html.** Joy's full drafted story (three to five short paragraphs, with spec facts only and `mark.confirm` for the name's origin, the moment it began, and a personal memory), the founder quote, the four credentials, mission and vision (verbatim from the current site), and the five steps Listen/Partner/Collect/Deliver/Report back.
- [ ] **Step 2: Write contact.html.** Contact cards (phone, email, Instagram), plus the form `<form data-wa="27815161673">` with name, organisation, `<select id="topic">` (values: `donate, sponsor, school, partner, volunteer, support`, with the labels from the current site), message, and a "Continue in WhatsApp ↗" button.
- [ ] **Step 3: Run the checker.** Expected: PASS for both. Manually open `contact.html?topic=volunteer`: Volunteer should be selected. `?topic=xyz` should show the first option. Submitting with an empty organisation and the message `it's 🎉` should open a wa.me URL with encoded text and no Organisation line.

### Task 4: Programmes + Get Involved pages

**Files:** Create `site/programmes.html`, `site/get-involved.html`

- [ ] **Step 1: Write programmes.html.** Four sections with ids `outreach, parcels, clothing, dignity`, each with 1–3 photos (outreach: class/mentor/books; parcels: parcels; clothing: clothing/navy/maroon/blue; dignity: cd1–3), what it is, who it serves, and a "Help with this →" link to `contact.html?topic=…`.
- [ ] **Step 2: Write get-involved.html.** Six route cards with ids `donate, sponsor, school, partner, volunteer, support`. Each says what's needed (from the current site's copy) and links to `contact.html?topic=<same id>`.
- [ ] **Step 3: Run the checker.** Expected: PASS.

### Task 5: Impact page

**Files:** Create `site/impact.html`

- [ ] **Step 1: Write impact.html.** Known true figures: 2022 (registered), 4 programmes, 3 spaces (schools, churches, campuses). One commented block `<!-- IMPACT FIGURES: fill data-value, remove hidden -->` with `hidden` slots for `parcels, boxes, learners, items`. Below that, photo stories per drive (the Comfort & Dignity Drive is featured), with descriptive captions only, plus the five-step "how a drive happens" summary linking to about.html.
- [ ] **Step 2: Run the checker on the whole site.** Expected: `OK` and exit 0.

### Task 6: Polish, SEO, package, handover

**Files:** Modify all six pages. Create `HANDOVER.md`, `dist/ncf-site-preview.zip`, `tools/package.py`

- [ ] **Step 1: Add per-page Open Graph tags** (`og:title`, `og:description`, `og:image` → `images/founder.jpg`), a favicon (`images/logo.jpg`), and NGO JSON-LD on index.html (name, url placeholder, email, telephone, sameAs Instagram).
- [ ] **Step 2: Do a visual check.** Serve with `python3 -m http.server -d site 8080` and look at each page at 360px and 1280px in the browser, in light and dark mode. Expected: no horizontal scroll, no blurry upscaled photos, the menu works, and the markers are visibly highlighted.
- [ ] **Step 3: Write `tools/package.py`.** It zips the contents of `site/` (files at the zip root) into `dist/ncf-site-preview.zip` and refuses to run if the checker fails.
- [ ] **Step 4: Write `HANDOVER.md`.** It covers: uploading to cPanel `/preview` + Directory Privacy; where Joy's markers are (`grep -n "Joy to confirm" site/*.html`); how to fill in the impact figures; and the launch steps (remove the markers, delete the noindex meta on all pages, set the JSON-LD url, upload to `public_html`).
- [ ] **Step 5: Run** `python3 tools/package.py`. Expected: the checker prints OK and the zip is created.
