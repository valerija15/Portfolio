# Anna Bērziņa — PR Portfolio

A bilingual (LV/EN) editorial portfolio for a Public Relations Specialist, built with **Astro 7**, TypeScript and plain CSS design tokens. Everything is static HTML. Client-side JavaScript is limited to small enhancement scripts: the mobile menu, language memory, scroll reveals, filters, the lightbox, video play/pause and the contact form.

> **All content is fictional placeholder content.** The person, clients, outlets, quotes and figures are invented. To go live, edit the files under `src/content/`, `src/i18n/` and `public/`. You never need to touch the components.

---

## Contents

1. [Running locally](#running-locally)
2. [Deploying](#deploying)
3. [Project structure](#project-structure)
4. [Adding or editing a project](#adding-or-editing-a-project)
5. [Replacing images and videos](#replacing-images-and-videos)
6. [Editing translations](#editing-translations)
7. [Configuring the contact form](#configuring-the-contact-form)
8. [Changing colours and fonts](#changing-colours-and-fonts)
9. [Other content (experience, media, testimonials, site config)](#other-content)
10. [Placeholder media sources](#placeholder-media-sources)
11. [Go-live checklist](#go-live-checklist)

---

## Running locally

Requirements: **Node 22+** (see `.nvmrc`).

```bash
npm install
```

```bash
npm run dev
```

The dev server runs at <http://localhost:4321>; `/` redirects to `/lv/`.

```bash
npm run build
```

`npm run build` type-checks the content (`astro check`) and then builds into `dist/`. Use `npm run build:fast` to skip the type check.

```bash
npm run preview
```

`npm run preview` serves the production build locally.

Content schemas are enforced at build time. A missing translation, a malformed date or a broken image path fails the build with a clear error, so it can never reach production.

## Deploying

The output is a fully static `dist/` folder. Two settings, both environment variables, control the URLs written into the build (canonical, hreflang, Open Graph, sitemap and every internal link):

| Variable | Meaning | Default |
| --- | --- | --- |
| `SITE_URL` | Origin the site is served from | `https://anna-berzina.example.com` |
| `BASE_PATH` | Sub-path, if the site doesn't live at the domain root | `/` |

### GitHub Pages (set up in this repo)

`.github/workflows/deploy-pages.yml` builds and deploys on every push to `main`. The site is served at **https://valerija15.github.io/Portfolio/**, and the workflow sets `SITE_URL` and `BASE_PATH=/Portfolio` automatically.

One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**. After that, each push to `main` deploys within a couple of minutes. You can watch it under the **Actions** tab, or re-run it manually with **Run workflow**.

For a custom domain on Pages, add it under **Settings → Pages → Custom domain**. Then change the workflow env to `SITE_URL: https://your-domain.lv` and `BASE_PATH: /`.

### Netlify

1. Log in at app.netlify.com → **Add new site → Import an existing project → GitHub**, and pick this repo.
2. Netlify reads `netlify.toml`: build command `npm run build`, publish directory `dist`, Node 22. Nothing to fill in.
3. Under **Site configuration → Environment variables**, add `SITE_URL` = your Netlify URL (e.g. `https://anna-berzina.netlify.app`) or custom domain. Leave `BASE_PATH` unset, because Netlify serves from the root.
4. Deploy. Every push to `main` redeploys, and pull requests get preview URLs.
5. Optional: add a custom domain under **Domain management**. HTTPS is automatic.

Netlify also offers form handling without a third-party service (see [Configuring the contact form](#configuring-the-contact-form)). `public/_headers` adds security headers and long-term caching for hashed assets.

### Vercel / Cloudflare Pages

- **Vercel:** import the repo. The Astro preset is auto-detected (build `npm run build`, output `dist`). Set `SITE_URL`.
- **Cloudflare Pages:** framework preset "Astro", build `npm run build`, output `dist`, env `NODE_VERSION=22` and `SITE_URL`.

All hosts serve `dist/404.html` for unknown URLs.

> Use the site's links/helpers rather than hard-coded "/…" paths when editing components. Root-relative paths in content (`/video/…`, `cvPath`, `ogImage`) are prefixed with `BASE_PATH` automatically.

## Project structure

```
src/
  content.config.ts        ← typed schemas (zod) for every collection
  content/
    site/site.yaml         ← name, title, contacts, socials, form endpoint, CV path, hero + about copy
    projects/*.yaml        ← one file per project (case studies)
    publications/*.yaml    ← media & publications
    experience.yaml        ← work history
    education.yaml         ← education & certifications
    testimonials.yaml      ← quotes
  i18n/lv.json, en.json    ← all UI strings, page titles & meta descriptions
  assets/images/           ← source images (optimised to AVIF/WebP at build)
  assets/fonts/            ← self-hosted, subset variable fonts (fingerprinted at build)
  styles/tokens.css        ← colours, type scale, spacing, motion
  styles/fonts.css         ← @font-face declarations
  components/, layouts/    ← presentation only, no copy
  pages/[lang]/...         ← routes, generated for /lv/ and /en/
public/
  video/                   ← self-hosted MP4/WebM loops
  cv/anna-berzina-cv.pdf   ← downloadable CV
  og/og-default.jpg        ← default social share image
scripts/
  generate-placeholders.py ← regenerates placeholder media (not needed once real assets exist)
  optimize-fonts.py        ← rebuilds the subset fonts
```

Routes: `/lv/` and `/en/` × Home, About (`about/`), Work (`work/`), project detail (`work/<slug>/`), Experience, Media, Contact and Privacy, plus a bilingual `/404.html`. Slugs are the same in both languages, so the LV|EN switcher always lands on the same page.

## Adding or editing a project

1. Copy an existing file in `src/content/projects/`, e.g. `nordlys.yaml` → `my-project.yaml`.
2. Edit the fields. Every human-readable field takes both `lv` and `en`:

```yaml
slug: my-project              # URL: /lv/work/my-project/ and /en/work/my-project/
placeholder: false            # true shows the "fictional figures" note under results
featured: true                # show on the home page (first 6 featured, by order)
order: 9                      # position in lists (ascending)
layout: large                 # tile hint: large | tall | wide | standard
year: 2026
category: media-relations     # pr-campaign | media-relations | event-communication | brand-communication
                              # social-media | content-creation | public-events | crisis-communication
client: Client name
role: { lv: …, en: … }
title: { lv: …, en: … }
summary: { lv: …, en: … }     # also used as the meta description
cover:                        # image…
  type: image
  src: ../../assets/images/projects/my-project-cover.jpg
  alt: { lv: …, en: … }
# cover:                      # …or a muted looping video
#   type: video
#   src: /video/my-loop.mp4
#   webm: /video/my-loop.webm      # optional
#   poster: ../../assets/images/projects/my-project-cover.jpg
#   alt: { lv: …, en: … }
overview:  { lv: "Markdown…", en: "Markdown…" }   # optional sections: overview, challenge, strategy, execution
results:                                          # optional; large stat figures
  - value: "+240%"
    label: { lv: mediju sasniedzamība, en: media reach }
gallery:                                          # optional; opens in the lightbox
  - type: image
    src: ../../assets/images/projects/my-project-1.jpg
    alt: { lv: …, en: … }
    caption: { lv: …, en: … }                     # optional
  - type: video                                   # self-hosted
    src: /video/clip.mp4
    poster: ../../assets/images/projects/my-project-2.jpg
    alt: { lv: …, en: … }
  - type: embed                                   # YouTube/Vimeo, click-to-load facade
    embed: { provider: youtube, id: VIDEO_ID }    # or { provider: vimeo, id: 123456789 }
    poster: ../../assets/images/projects/my-project-3.jpg
    alt: { lv: …, en: … }
links:                                            # optional; open in a new tab
  - title: { lv: …, en: … }
    url: https://…
    outlet: Outlet name
```

Every section is optional. A project page only renders the sections that have data. Previous/next navigation follows `order` and wraps around. Category filter buttons only appear for categories that are in use. Filtered views are shareable, e.g. `/en/work/?category=crisis-communication`.

## Replacing images and videos

**Images:** put files in `src/assets/images/` (any sub-folder) and reference them with a path **relative to the YAML file** (e.g. `../../assets/images/projects/x.jpg`). Astro generates AVIF/WebP `srcset`s with width/height at build time. Use high-resolution originals (≥ 2000 px on the long side for covers). Recommended aspect ratios, which the layout crops gracefully if you use others:

| Use | Ratio |
| --- | --- |
| Hero portrait (`site.yaml › hero.media`) | 4:5 |
| About portrait / teaser | 3:4 / 1:1 |
| Project covers | `large` 4:3 · `tall` 4:5 · `wide` 2:1 · `standard` 5:4 |
| Gallery | any (3:2, 4:5, 4:3, 16:9 all work) |
| Publication thumbnails / video posters | 16:9 |

The simplest way to swap an image is to overwrite the file with the same name. To use another name, update the path in the YAML.

**Videos:** put muted loops in `public/video/` and reference them as `/video/name.mp4`. Keep them short (6–12 s), muted, H.264 MP4 (+ optional VP9 WebM) at around 1280–1920 px wide and under ~3 MB. Every video **must** have a `poster` image. Cover loops autoplay only while on screen, never under `prefers-reduced-motion`, and always show a pause/play button.

```bash
ffmpeg -i in.mov -an -vf "scale=1600:-2" -c:v libx264 -crf 26 -preset slow -movflags +faststart out.mp4
```

```bash
ffmpeg -i in.mov -an -vf "scale=1600:-2" -c:v libvpx-vp9 -crf 38 -b:v 0 out.webm
```

These commands produce the MP4 and WebM versions.

**Hero video variant:** in `site.yaml`, replace `hero.media` with the commented `type: video` block. `public/video/hero-loop.mp4` is ready to try.

**Social image:** replace `public/og/og-default.jpg` (1200×630). Project pages automatically use a 1200×630 crop of their cover.

**CV:** replace `public/cv/anna-berzina-cv.pdf`, or change/remove `cvPath` in `site.yaml`. Removing it hides the download button.

**Outlet logos:** publications render a typographic wordmark by default (`outlet.wordmark: serif | sans | italic | mono | condensed`). To use a real logo (with permission), add `outlet.logo: ../../assets/images/logos/outlet.svg`.

## Editing translations

- **UI strings, page titles and meta descriptions:** `src/i18n/lv.json` and `src/i18n/en.json`. Both files must have identical keys. A missing key throws at build time and names the key. `{placeholders}` such as `{n}` or `{email}` are filled in by the code.
- **Content:** every content field is a `{ lv, en }` pair in the YAML files. Long text fields (`overview`, `challenge`, `strategy`, `execution`, `about.bio`, `privacy.body`) accept Markdown.
- **Dates** are formatted per locale with `Intl.DateTimeFormat` (`lv-LV`, `en-GB`). Write experience dates as `YYYY-MM`; leave `end: null` for "present".
- **Language behaviour:** URLs are the source of truth. The visitor's last language is stored in `localStorage` (`preferred-lang`) only to redirect the bare `/`. Every page sets `<html lang>`, a canonical URL, `hreflang` alternates (incl. `x-default` → LV) and a localised `<title>`/description.

To add a third language, add it to `LOCALES` in `src/i18n/index.ts`, create `src/i18n/<code>.json` and add the `<code>` field to the `localized` schema in `src/content.config.ts`. The build then lists every missing string.

## Configuring the contact form

All settings are in `src/content/site/site.yaml`:

```yaml
form:
  provider: formspree         # formspree | netlify | custom | none
  endpoint: "https://formspree.io/f/abcdwxyz"
```

| Provider | What to do |
| --- | --- |
| **none** (default) | No endpoint is needed. The button opens the visitor's email app with a prefilled `mailto:` (subject + message + name/email). It is never a dead button. |
| **formspree** | Create a form at formspree.io and paste its endpoint. The site POSTs `FormData` with `Accept: application/json`. |
| **netlify** | Set `provider: netlify` (endpoint can stay empty). The form carries `data-netlify` and a honeypot. Enable form detection in the Netlify UI. |
| **custom** | Any endpoint that accepts a POST with `multipart/form-data` and returns 2xx on success. |

The form provides:

- Accessible validation: inline errors are linked with `aria-describedby`, an error summary is announced, and focus moves to the first invalid field.
- A hidden honeypot field (`company_website`) for spam.
- Loading, success and error states in both languages.
- A GDPR consent checkbox linking to the privacy notice.

Without JavaScript the browser's native validation and a plain POST (or `mailto:`) still work.

## Changing colours and fonts

All design decisions are tokens in `src/styles/tokens.css`:

```css
--color-paper: #f4f2ec;   /* background */
--color-ink: #141413;     /* text / black */
--color-charcoal: #2b2a28;/* dark bands, footer */
--color-accent: #9a4a2f;  /* the ONE accent (muted terracotta) */
--color-accent-soft: #d99a7c; /* accent on dark backgrounds */
```

- Swap the accent for, e.g., deep olive `#4f5a2e` / soft `#b8c08f`. Keep text contrast ≥ 4.5:1 on `--color-paper` (WCAG AA).
- The type scale (`--step--1` … `--step-6`) is fluid between 360 px and 1440 px. Spacing (`--space-*`), gutters, max width and motion durations are tokens too. Motion durations collapse to `0ms` under `prefers-reduced-motion`.

**Fonts:**

- Display: **Newsreader** (variable, opsz + wght). Body: **Hanken Grotesk** (variable).
- Both are SIL OFL fonts, self-hosted in `src/assets/fonts/` with `font-display: swap`.
- Both are verified to include all Latvian letters: ā č ē ģ ī ķ ļ ņ š ū ž (and capitals).
- The files are subset and axis-limited by `scripts/optimize-fonts.py`.

To change fonts:

1. Put the new `.woff2` files in `src/assets/fonts/` and update the relative `url()`s in `src/styles/fonts.css`.
2. Update `--font-display` / `--font-body` in `tokens.css`.
3. Update the two font `?url` imports used for `<link rel="preload">` in `src/layouts/BaseLayout.astro`.

> When splitting a font into `latin` / `latin-ext` files, keep combining marks (U+0300–036F) **out** of the `latin` `unicode-range`. Otherwise Chrome may draw "ī" as *i + floating macron* instead of the proper glyph.

## Other content

| File | What it holds |
| --- | --- |
| `src/content/site/site.yaml` | Name, title, location, email, phone (`showPhone`), LinkedIn, form, CV path, hero headline (two lines) + intro + media, about lead/bio/teaser, principles (1–6), expertise list |
| `src/content/experience.yaml` | Organisation, position, location, `start`/`end` (`YYYY-MM`, `null` = present), description, achievements |
| `src/content/education.yaml` | `kind: education \| certification`, institution, qualification, dates |
| `src/content/publications/*.yaml` | `type` (article, press-release, interview, media-appearance, campaign-publication, video-interview), title, date, url, language, outlet, optional thumbnail, optional `video: { provider, id }` (shown with the click-to-load facade), `highlight: true` to show the outlet on the home page strip |
| `src/content/testimonials.yaml` | Quote, name, role, organisation; `fictional: true` shows an "illustrative" note. Set it to `false` only for real, approved quotes. |

## Placeholder media sources

The build environment had no access to Unsplash or Pexels. To keep the repository self-contained and licence-clean, **all placeholder images and videos are generated locally** by `scripts/generate-placeholders.py` (Python + Pillow + ffmpeg):

- Muted, tonal compositions (backlit portraits, stages and audiences, press clippings, studio microphones, still lifes) with film grain, at realistic aspect ratios.
- Video loops are slow push-ins built from those stills (`public/video/*.mp4|webm`), each with a poster.
- No third-party trademarks. Outlets and brands are fictional and rendered as text wordmarks.
- The YouTube embeds use the Blender Foundation's open movie *Big Buck Bunny* (`aqz-KE-bpKQ`, CC BY 3.0) as a stand-in ID. Replace these with the real video IDs.

To use stock photography instead, download from these Unsplash/Pexels searches (free licence) and keep the file names:

| Placeholder file | Suggested search |
| --- | --- |
| `portrait-hero.jpg`, `portrait-about.jpg`, `portrait-teaser.jpg` | "editorial portrait woman natural light" |
| `projects/*-cover.jpg` (audience/stage) | "conference stage audience", "event speaker spotlight" |
| `projects/*` (press) | "newspaper on table", "press clipping" |
| `projects/*` (studio) | "podcast microphones studio", "tv interview studio" |
| `projects/*` (still life / abstract) | "minimal still life ceramics", "architecture abstract shapes" |
| `media/interview-*.jpg` | "interview set lighting" |
| `public/video/*` (Pexels Videos) | "city lights night", "conference crowd", "harbour cranes" |

Record each final asset's source URL and licence here before launch.

Run `npm run media:placeholders` to regenerate the placeholders.

## Go-live checklist

- [ ] Replace every YAML file in `src/content/` (each file is marked `PLACEHOLDER`). Set `placeholder: false` on projects and `fictional: false` only on real testimonials.
- [ ] Replace images in `src/assets/images/`, videos in `public/video/`, `public/og/og-default.jpg` and `public/cv/…pdf`.
- [ ] Set the email, phone, LinkedIn and form endpoint in `site.yaml`.
- [ ] Set `SITE_URL` on the host.
- [ ] Review `privacy.body` in both i18n files with the actual data processor.
- [ ] **Analytics:** none are included, so no cookie banner is needed. If you add analytics or any non-essential cookies/trackers, a **consent banner becomes legally required** (GDPR/ePrivacy). Load the scripts only after consent and update the privacy notice.

## Quality notes

- Lighthouse (mobile, local static server, no compression): Performance 94–100, Accessibility 100, Best Practices 100, SEO 100 on the pages tested.
- WCAG 2.2 AA:
  - Skip link, landmarks and heading order.
  - Visible focus styles and AA contrast tokens.
  - Full keyboard operation; the menu and lightbox use modal `<dialog>`, which contains focus, closes on Esc and returns focus.
  - Alt text on every image.
  - Reduced-motion support.
  - Pause controls on looping video.
- SEO:
  - Unique localised titles and descriptions, canonical URLs and `hreflang`.
  - Open Graph and Twitter cards.
  - `sitemap-index.xml` with alternates and `robots.txt`.
  - JSON-LD `Person` (home) and `CreativeWork` (projects).
