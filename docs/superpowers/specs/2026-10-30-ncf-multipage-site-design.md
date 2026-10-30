# NCF multi-page website: design

Date: 2026-10-30
Client: Nonkululeko Catherine Foundation (NCF), a registered NPO in KwaZulu-Natal, since 2022
Built by: Lubelo Tech Solutions

## Intent and the why

Turn the current single-page site (`index.html`) into a clean, modern **multi-page** website and put it live.

The client's main goal is **impact**. A visitor should *feel* what the foundation does, so they stay on the site and then help. In the client's words, it should be "something touching that will make someone stay on the website."

The emotional anchor is chosen: the homepage opens on **the founder, Joy, and the personal reason the foundation exists** ("the why behind the name"). It should read like a letter from a person, not a charity advert.

## Goals

- Visitors feel the human reason behind NCF within the first screen of the homepage.
- Every page leads to a clear way to help (donate items, sponsor a comfort box, volunteer, partner, invite NCF to a school, ask for support).
- The site is clean and modern, with lots of white space and calm pages, and stays on-brand.
- It works well on phones first, since most visitors will arrive from Instagram and WhatsApp.
- It goes live on the foundation's cPanel hosting, after a private preview that Joy approves.

## Non-goals

- No CMS, admin panel, user accounts, or online payments. Donations go through contact or WhatsApp, as they do today.
- No blog or news system.

## Anti-goals (a failure even if it technically works)

- **No invented stories, quotes, people or numbers presented as real.** The founder's story is a draft. Every detail not already known is marked `[Joy to confirm]` and must be replaced by Joy before launch. Placeholder student quotes from the mockups must not appear.
- Blurry, stretched photos. The source images are small (most are under 610px wide), so no full-bleed photo heroes.
- Heavy, slow pages, or a design that looks like a generic template.

## Known, true content (from the current `index.html`)

Use this as the source of facts. Reuse the copy where it fits.

- Tagline: "We care beyond measure." Hero line: "From care to change."
- About: a dedicated non-profit that mobilises youth, empowers communities, provides essential services, advocates for change and addresses social issues. Its primary focus is teenagers. It operates with transparency and accountability.
- Founder quote (real): "The idea and the vision became a reality. Then the hard work began, and a foundation was laid."
- Mission and vision text: as in the current site.
- Four programmes: School outreach & applications; Food parcels; The NCF Clothing Drive ("What you can spare, others can wear"); Comfort & Dignity Drive (personal-care boxes for young women on university campuses).
- Five-step process: Listen, Partner, Collect, Deliver, Report back.
- Founder: Sinalenjabulo Joy Ndlovu, Founder & Director. Fourth-year HR Management student at DUT, HR professional, woman of faith. Credentials: Student Engagement Officer (DUT Student Woman Economic Empowerment Programme, 2025/26); Runner-up, Community Engagement Pitch Contest 2024; innobiz Incubation Programme; House Committee Member 2024/25.
- Partners: high schools, churches, universities, organisations.
- Contact: phone/WhatsApp 081 516 1673; email thenonkululekofoundation@gmail.com; Instagram @official_ncf. The existing form builds a WhatsApp message (wa.me) and should be kept.
- Footer credit: "Website by Lubelo Tech Solutions".

## Pages

1. **Home** (`index.html`): opens on Joy (portrait `founder.jpg`) with a short excerpt of her story and a link to read more. Then a short "From care to change" line, the four programmes as a glimpse, a strip of real photos, the six ways to help, and a closing call to action.
2. **Our Story** (`about.html`): Joy's full story (drafted, with `[Joy to confirm]` markers), the founder quote, her credentials, the mission and vision, and the five-step "how a drive happens".
3. **Programmes** (`programmes.html`): one section per programme with photos, what it is, who it serves, and how to help with that programme.
4. **Impact** (`impact.html`): photo stories from real drives (Comfort & Dignity using `cd1-3.jpg`, school outreach, food parcels, clothing). Only true numbers already known (registered 2022, 4 programmes, schools/churches/campuses). Clearly marked slots for real figures from Joy (e.g. parcels delivered, boxes given, learners helped), which stay hidden until filled.
5. **Get Involved** (`get-involved.html`): the six routes from the current site, each with what's needed and a button that pre-fills the contact or WhatsApp form.
6. **Contact** (`contact.html`): phone, email, Instagram, and the WhatsApp message form.

Shared header with navigation and a prominent "Get involved" button, a mobile menu, and a shared footer on every page.

## Decided

- Story-first homepage, option B (the client chose it from mockups).
- Founder story is drafted by us. Joy checks and corrects it before launch (the client confirmed).
- Six pages as listed (the client approved).
- **Hosting: cPanel** (the client's choice). This is a plain static site uploaded to `public_html` (or the domain's folder).
- **Private preview first** (the client's choice). Nothing goes public until Joy approves the story. The preview shows the `[Joy to confirm]` markers visibly (highlighted), carries `<meta name="robots" content="noindex">`, and is uploaded to a password-protected subfolder (cPanel → Directory Privacy, e.g. `/preview`). For launch, remove the markers and the noindex tag, then upload to the root.
- Keep brand colours: plum/deep `#24123A`/`#2A1640`, magenta `#E4237C`, and the logo gradient (blue `#3E7CC4`, purple `#9B4DC8`, magenta, orange `#F08A2E`). Calmer and more white space than today.

## Builder's calls (made by us, the client can override)

- Plain static HTML/CSS with a little vanilla JS. No framework or build step. Shared CSS in one file.
- Deliverable: a ready-to-upload folder plus a `.zip` (cPanel File Manager can extract it), and a short `HANDOVER.md` saying where to edit Joy's story and the impact numbers.
- Impact figures live in one clearly commented block in `impact.html`, so they're easy to fill in safely. Empty slots stay hidden.
- The homepage's first screen must work before Joy's story exists. It leads with her photo, her real quote and the "why we exist" framing, with the drafted, marked excerpt below.
- The brainstorm mockup (option B) sets the structure only (founder photo beside a "why we exist" letter), not the final visuals.
- Typography, layout details, animation, and exact copy wording, within the anti-goals.
- Keep light/dark mode support from the current site.
- Basic SEO per page: title, description, Open Graph image, plus NGO schema on the home page.
- Images: optimise and size for their small originals. Use framed or card layouts, not full-bleed.

## Before launch checklist

- The preview is approved by Joy via the password-protected link.
- Joy replaces every `[Joy to confirm]` marker and approves the founder story.
- Every page has been checked on a phone-width screen.
- The WhatsApp form opens with the right number and message.
