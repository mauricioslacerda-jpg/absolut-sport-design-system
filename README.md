# ABSOLUT Sport — Design System

## Company Overview

**ABSOLUT Sport** is the *only official travel package agency* for the CONMEBOL Libertadores™ and CONMEBOL Sudamericana™ Finals. A multinational sportainment agency connecting fans, corporations, and sports delegations to legendary experiences at the world's greatest sporting events.

- **Founded:** ~2010 (14+ years of operation)
- **Offices:** Rio de Janeiro 🇧🇷 · Frankfurt 🇩🇪 · Los Angeles 🇺🇸 · Buenos Aires 🇦🇷
- **Scale:** +500 annual events · +10,000 annual trips · +30 international partners
- **Official partnerships:** CONMEBOL Libertadores™, CONMEBOL Sudamericana™, Copa América 2024
- **Tagline:** "Dos estádios para a história!" *(From the stadiums to history!)*
- **Alt tagline:** "ISSO É VIVER." *(THIS IS LIVING.)*

### Products / Surfaces
1. **Marketing Website** — `absolut-sport.com.br` (Shopify-based e-commerce + marketing site)
2. **Event Package Pages** — Libertadores, Sudamericana, F1, NFL, Tennis packages
3. **Social Media** — Instagram @absolutsportbr (65K followers)

### Sources Used
- Company description provided directly by client
- Public website: https://absolut-sport.com.br/ (Shopify store)
- CONMEBOL press release: https://www.conmebol.com/pt-br/noticias-pt-br/absolut-sport-e-a-agencia-oficial-das-finais-da-conmebol-libertadores-e-conmebol-sudamericana/
- Brand logo reference: https://whatthelogo.com/logo/absolut/49155
- Instagram: https://www.instagram.com/absolutsportbr/
- No Figma or codebase access was provided.

---

## CONTENT FUNDAMENTALS

### Language
- **Primary language:** Portuguese (Brazil) — all UI copy defaults to PT-BR
- **Secondary:** English and Spanish (multinational agency)

### Tone & Voice
- **Bold and aspirational** — copy is written with emotional charge ("experiências lendárias" / *legendary experiences*, "momentos inesquecíveis" / *unforgettable moments*)
- **Authoritative** — references to official status and credentials ("Única Agência Oficial" / *Only Official Agency*)
- **Warm but premium** — not cold luxury; passionate Brazilian energy with German precision
- **Second person (você)** — brand speaks directly to the customer
- **Exclamation heavy** — enthusiasm is part of the brand voice
- **Capitalized proper nouns** — CONMEBOL, ABSOLUT Sport, etc. always styled in caps/title case

### Casing
- Brand name: **ABSOLUT Sport** (ABSOLUT in caps, Sport in title case)
- Headlines: ALL CAPS or Title Case for major calls to action
- Body: Sentence case
- Taglines: ALL CAPS ("DOS ESTÁDIOS PARA A HISTÓRIA" / *FROM THE STADIUMS TO HISTORY*, "ISSO É VIVER" / *THIS IS LIVING*)

### Copy Examples
- "Somos a única agência oficial de pacotes para as Finais da CONMEBOL Libertadores™" *(We are the only official package agency for the CONMEBOL Libertadores™ Finals)*
- "Experiências esportivas lendárias" *(Legendary sporting experiences)*
- "Vivências imersivas e emocionantes que transcendem o jogo" *(Immersive, exciting experiences that transcend the game)*
- "Excelência, conforto e segurança" *(Excellence, comfort, and safety)*
- "O céu é o limite para que você viva experiências lendárias!" *(The sky's the limit for you to live legendary experiences!)*
- "Eficiência alemã, entusiasmo brasileiro e estilo de vida californiano" *(German efficiency, Brazilian enthusiasm, and California lifestyle)*

### Emoji Usage
- Used sparingly in social media contexts (🤝 for partnerships)
- NOT used in primary website UI or marketing materials

---

## VISUAL FOUNDATIONS

### Color System
- **Primary Blue:** `#155F97` — ASB Blue, primary institutional color, CTAs and highlights
- **Blue Dark:** `#0F4A75` — hover states, depth
- **Blue Mid:** `#1E7ABE` — dark-mode version of the primary blue
- **Blue Highlight:** `#2857F7` — accent highlight, hover emphasis
- **Black:** `#0D0D0D` — dark background, authority, premium
- **White:** `#FFFFFF` — text on dark backgrounds, clean surfaces
- **Off-White:** `#FAFAFA` — default light-mode background (primary mode)
- **Gray ASB:** `#C0C0C0` — institutional gray, secondary elements
- **Gold/Amber:** `#C9A84C` — premium tier, VIP badges, "official"
- **Error/Alert:** `#E3001B` — error states and critical alerts only

### Logo
- Mark: A stylized bold capital **"A"** (no crossbar) — monolithic, modern
- Red oval accent top-right of the "A" — like a ball or badge
- Wordmark: "Absolut" in bold uppercase sans-serif below the mark
- Color: Black on light backgrounds; White on dark; Red accent always preserved
- Usage: "ABSOLUT Sport" — never just "Absolut"

### Typography
- **Display / Headlines:** SoulCraft GX (variable, weight 900 for maximum impact) — the brand's primary typeface, high-voltage
  - Local font: `fonts/soulcraftgx.ttf` (included in `absolut-brand-kit.zip`)
  - Fallback: Barlow Condensed, sans-serif
  - Signature: include `zero-to-o.js` on any page using SoulCraft (swaps "0" for uppercase "O" — `+5oo`, `1oK`, `12o×`)
- **Body / UI:** Barlow (Regular/Medium/SemiBold) — clean, readable, modern
  - Fallback: DM Sans, Inter
  - Google Fonts (free, open): https://fonts.google.com/specimen/Barlow
  - Display fallback (free): https://fonts.google.com/specimen/Barlow+Condensed
- **Mono / Data:** JetBrains Mono — for prices, codes, stats
  - Google Fonts (free): https://fonts.google.com/specimen/JetBrains+Mono

> **Font access:** SoulCraft GX is bundled in `assets/absolut-brand-kit.zip` (download via the Hub). Barlow and JetBrains Mono are free on Google Fonts — anyone with access to the Hub can download them from the links above.

### Backgrounds & Imagery
- **Full-bleed photography** is a core visual tool — stadium crowds, aerial shots, dramatic night games
- **Dark overlay gradients** over photos (bottom-to-top or radial from center) — ensures legibility
- **Dark-mode first** — the brand defaults to dark backgrounds; light mode is rare
- Imagery color vibe: warm-tinted highlights, dramatic contrast, stadium lights at night
- No hand-drawn illustrations; no flat decorative patterns
- Subtle texture via noise/grain overlays on dark cards

### Layout & Spacing
- Grid: 12-column, max-width 1280px, generous padding (80px+ section padding on desktop)
- Mobile-first sections: full-bleed hero → stat strip → card grid → CTA
- Generous white space between sections; content is NOT cramped
- Event cards: horizontal or vertical, with full-bleed photo + overlay text

### Borders & Radius
- Cards: `border-radius: 8px` (subtle)
- Buttons: `border-radius: 4px` (nearly square — athletic, not bubbly)
- Badges/pills: `border-radius: 100px` (full pill)
- No heavy rounded-corner cards with colored left-border accent

### Shadows & Elevation
- Cards: `box-shadow: 0 4px 24px rgba(0,0,0,0.4)` — deep, dramatic on dark backgrounds
- Modals/floating: `0 8px 48px rgba(0,0,0,0.6)`
- No light/soft shadows — everything is bold and substantial

### Animation & Interaction
- Subtle transitions: `0.2s ease-out` for hover states
- Hover on cards: slight scale-up (`scale(1.02)`) + brightness boost
- Hover on buttons: background darkens or shifts to solid from outlined
- Press states: scale down slightly (`scale(0.97)`)
- No bouncy/spring animations; energetic but controlled

### Buttons
- **Primary CTA:** Solid red `#E3001B`, white text, bold — "COMPRAR PACOTE", "VER PACOTES"
- **Secondary:** Outlined white border, white text, transparent background
- **Ghost/subtle:** Transparent with light text for tertiary actions
- Buttons are uppercase, bold, no icons unless critical

### Iconography — See ICONOGRAPHY section below

---

## ICONOGRAPHY

- No proprietary icon font detected (website built on Shopify theme)
- Icons used are likely **SVG inline** or a generic icon set
- Functional icons: checkmarks ✓ for feature lists, arrows for navigation, social icons
- **Substitution used:** Lucide Icons (CDN) — clean, 2px stroke weight, modern geometric
  - CDN: `https://unpkg.com/lucide@latest`
- No emoji used as iconography in professional marketing materials
- Social: Instagram, WhatsApp icons appear prominently (WhatsApp is primary contact channel in Brazil)
- Trophy, stadium, airplane, hotel, ticket icons used contextually for service features

### Asset Inventory
See `assets/` folder:
- `assets/logo-azul-preto.svg` — **Primary** · Blue + Black logo · light backgrounds (light mode)
- `assets/logo-azul-branco.svg` — Blue + White logo · dark backgrounds (dark mode)
- `assets/logo-branco.svg` — Monochrome white logo · blue or dark backgrounds
- `assets/logo-preto.svg` — Monochrome black logo · B&W print · light backgrounds

---

## SKILL INDEX

| File | Description |
|------|-------------|
| `docs/` | **Published Hub root** — everything GitHub Pages serves lives here (source path `/docs` on `main`). All entries below are relative to this folder. |
| `docs/index.html` | **Design System Hub** — public page for the whole company. Logos, colors, typography, tokens, components, guidelines, and dev resources. Live at the GitHub Pages URL below; a dedicated subdomain (e.g. `design.absolut-sport.com.br`) is a possible future upgrade. |
| `docs/playbooks/ai-marketing.html` | **AI Marketing Playbook** — child page of the Hub, aimed at the global marketing team. |
| `docs/playbooks/content-growth.html` | **Content Growth Playbook** — child page of the Hub. The owned blog: Shopify architecture, AEO anatomy, the production engine, PR pitch audit, and channel economics (Hormozi). Deep-dive behind the "SEO / Content" card in Growth. Canonical in PT (i18n EN/ES/DE = BL-006). |
| `docs/playbooks/content-growth.md` | **Content Growth · CANONICAL (playbook doc)** — text version of the blog playbook. References `cross-sell-taxonomy.md` (silos) and the deep strategy in the vault. Standard for the taxonomy suite. |
| `docs/playbooks/` | Folder for applied playbooks (each one is a child page of the Hub). |
| `docs/email-command-center.html` | **Email Marketing · Command Center** — internal dashboard for the email marketing project. 10 tabs (Overview · Master Strategy · 6 legacy silos · Tracking · Templates). ⚠ Migrating to the new taxonomy (7 silos + 2 programs, 3 levels: silo/sub-silo/event) — see `docs/playbooks/cross-sell-taxonomy.md` and `docs/playbooks/growth-email.html`. ABSOLUT brandbook applied: tokens, SoulCraft, Lucide. Operational tool for the Growth team. |
| `docs/playbooks/cross-sell-taxonomy.md` | **Cross-Sell Taxonomy · CANONICAL** — canonical 3-level taxonomy model (silo → sub-silo → event), affinity matrix between sub-silos, trigger rules for RD Station automation. Version 1.0 · May 2026. |
| `docs/playbooks/cross-sell-matrix.csv` | **Affinity matrix · 169 pairs** — origin/destination/score in long format. Ready for Victor to import into RD Station. Accompanies the canonical doc. |
| `docs/playbooks/taxonomy-takeaway.md` | **1-page takeaway · For Daniel + stakeholders** — jargon-free explanation of the new taxonomy: what changed, why it changed, what didn't change. 3-minute read. |
| `docs/playbooks/taxonomy-quick-reference.md` | **Quick Reference · For Jack, Rachella, Victor, Wictor** — pocket card: the 3 levels, the 7 silos, the 8 questions to ask before writing an email, condensed cross-sell matrix, standard frontmatter. Print it and tape it to your desk. |
| `docs/playbooks/taxonomy-folder-template.md` | **Folder template · For Wictor + Drive** — complete physical Drive structure following the taxonomy. Includes checklists for creating a new event, sub-silo, or silo. Non-negotiable principles. |
| `docs/playbooks/copy-library.html` | **Copy Library · Aby — Quick-Reply Library** — 35 messages across 13 categories with a variable system for reuse per event. Category filter, search, copy-to-clipboard, i18n PT/EN/ES/DE. Living page fed by JSONs generated via `docs/playbooks/copy-library/extract.py`. Source: canonical spreadsheet (gid 1469143387). |
| `docs/playbooks/copy-library/` | Structured data and generator script: `extract.py` (spreadsheet parser), `input.tsv` (source), `messages.json` + `variables.json` (data), `i18n-{pt,en,es,de}.json` (dictionaries). See `docs/playbooks/copy-library/README.md`. |
| `README.md` | This file — brand overview, fundamentals, index. |
| `docs/colors_and_type.css` | CSS custom properties for all design tokens. **Import into pages via `<link>`.** |
| `docs/zero-to-o.js` | Script that swaps "0" for uppercase "O" in SoulCraft text (the brand's signature). Include on any page using SoulCraft. |
| `docs/fonts/soulcraftgx.ttf` | SoulCraft GX display font. |
| `docs/preview/` | Preview cards for each component (linked from the Hub). |
| `docs/assets/` | Logos and brand assets (.svg). |
| `docs/assets/absolut-brand-kit.zip` | **Complete Brand Kit** — 4 logos + SoulCraft GX + colors_and_type.css + zero-to-o.js + README. Linked from the Hub via the "Brand Kit" CTA. Regenerate via PowerShell `Compress-Archive` whenever tokens/logos/font are updated. |
| `docs/assets/rafa-rafa.png` | Poster art for the "Ask Rafa" banner in the Hub footer. Also used as `og:image` on every page. |
| `docs/assets/mauricio.jpg` | _TODO_: photo of Mauricio Lacerda. Reserved for planned use (co-authorship banner, coordination profile, or expanding the Rafa Rafa banner into a duo). Kept in the repo pending a decision on use. |
| `docs/ui_kits/website/` | React UI kit for absolut-sport.com.br. |
| `SKILL.md` | **Brandbook Skill (Claude)** — full brandbook spec in Claude skill format. Loads color rules, typography, icons (Lucide), motion, Mauricio's voice, i18n, applied playbooks, anti-patterns, and contact info. See the "Claude Skill" section below to activate it locally. |
| `I18N_METHOD.md` | Replicable translation method (i18n.js + inline dictionary). Use the same pattern on other projects. |

---

## SKILL CLAUDE · BRANDBOOK

`SKILL.md` is the canonical brandbook in Claude skill format. When activated, it loads the full context: colors, typography, logos, iconography rules (Lucide), motion, Mauricio's voice, i18n across the 4 languages, applied playbooks, and anti-patterns.

### What it's for

Any Claude (Code, Desktop, API) with the skill activated will generate visual and text artifacts already aligned with the ABSOLUT Sport brandbook — no need to repeat the rules in every conversation. It covers:

- Landing pages, emails, decks, social media
- Copy in PT/EN/ES/DE with Mauricio's voice
- Production-ready HTML with design system tokens and components
- Prompts for AI tools (Midjourney, ChatGPT, etc.) already formatted with brand context

### Activate locally (Claude Code)

Copy the entire folder into the Claude Code skills directory:

```powershell
$src = "G:\Meu Drive\ABSOLUT Sport Design System"
$dest = "$env:USERPROFILE\.claude\skills\absolut-sport-design"
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Copy-Item -Path $src -Destination $dest -Recurse
```

The skill is auto-discovered via `SKILL.md`. Activate it via `/skills` in Claude Code, or invoke it directly in conversation when needed.

### Updating the skill

Did something change in the design system (a new token, a new aphorism, an anti-pattern to document)? Edit `SKILL.md` at the project root. Re-run the `Copy-Item` command above to propagate it.

The skill can also be installed via direct download of `SKILL.md` + its referenced files from the live Hub at `https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/`.

### Usage triggers (when the skill activates)

The `description` in the frontmatter includes keywords that trigger the skill when relevant:
- "ABSOLUT Sport", "CONMEBOL Libertadores", "Sudamericana"
- "landing page", "email template", "deck", "social media", "voucher"
- "marketing copy", "brand colors", "logo"
- "Mauricio", "Rafa Rafa", "design@absolut-sport.com.br"

---

## DEPLOY — How to publish

The Hub is a static page — no build step, no application server. It is published via **GitHub Pages**, serving the `docs/` folder on the `main` branch.

### Where things live

- **Live URL (canonical today):** `https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/`
- **Repo:** `github.com/mauricioslacerda-jpg/absolut-sport-design-system` — Pages source: branch `main`, path `/docs`
- **Future upgrade (not yet implemented):** a dedicated subdomain (e.g. `design.absolut-sport.com.br`) via CNAME pointed at the GitHub Pages URL, or a Shopify embed at `https://absolut-sport.com.br/pages/design-system`
- **Contact email:** `design@absolut-sport.com.br` (suggestions, changes, questions)

### Publishing steps

Publishing is just pushing to `main` — GitHub rebuilds Pages automatically from `docs/`.

1. **Edit files under `docs/`** — `docs/index.html` is the entry point. All paths are relative (`./assets/...`, `./fonts/...`, `./preview/...`), so the site works both locally (open the file) and under the repo's Pages subpath.
2. **Commit and push to `main`.** GitHub Pages rebuilds within ~1 minute; check status via `gh api repos/mauricioslacerda-jpg/absolut-sport-design-system/pages`.
3. **Custom domain (optional, later):** add a `CNAME` file to `docs/` with the desired hostname, then create a DNS CNAME record pointing that hostname at `mauricioslacerda-jpg.github.io`. Requires access to the domain's DNS panel.

### Embedding in Shopify

In the Shopify admin → Pages → create a new page with the handle `design-system`. Content (HTML view):

```html
<iframe
  src="https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/"
  title="ABSOLUT Sport Design System"
  loading="lazy"
  style="display:block;width:100%;height:calc(100vh - 120px);border:none;"
  allow="clipboard-write"
></iframe>
```

GitHub Pages does not send restrictive `X-Frame-Options`/CSP headers by default, so the iframe should load as-is.

### Co-authorship and contact

The design system is **co-authored by Mauricio Lacerda × Raphael Ferreira (Rafa Rafa)**. Credit is visible in the header (gold "MM × RR" badge) and in the footer of every page. For any change, suggestion, or request: `design@absolut-sport.com.br`.

### Access

Public link — anyone with the URL can access it. Brand guidelines are freely distributed across the 4 offices (Rio, Frankfurt, LA, Buenos Aires).

### Supported languages

Toggle in the top-right corner of every page. The preference persists in `localStorage` (`asb_lang`).

| Code | Language | Primary market |
|---|---|---|
| `pt` | Português (BR) | Rio de Janeiro · default |
| `en` | English | Los Angeles · global |
| `es` | Español | Buenos Aires · LATAM |
| `de` | Deutsch | Frankfurt |

---

## HIERARCHICAL STRUCTURE

```
ABSOLUT Sport Design System/
├── README.md                        ← This file
├── BACKLOG.md                       ← Pending ideas (BL-001…)
├── SKILL.md                         ← Claude brandbook skill
├── ASB_Design_Token_Taxonomy_v1.md
├── I18N_METHOD.md
└── docs/                            ← Published root (GitHub Pages: main, /docs)
    ├── index.html                   ← Main Hub (public)
    ├── colors_and_type.css          ← Canonical tokens (import)
    ├── zero-to-o.js                 ← Typographic signature
    ├── playbooks/
    │   ├── ai-marketing.html        ← AI Playbook (Global Marketing)
    │   └── ...                      ← other applied playbooks
    ├── preview/                     ← component preview cards
    ├── ui_kits/website/             ← React UI kit for the public site
    ├── assets/                      ← logo variants (.svg) + brand kit
    └── fonts/                       ← SoulCraft GX
```
