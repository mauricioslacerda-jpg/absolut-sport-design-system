---
name: absolut-sport-design
description: Use this skill whenever generating any visual or textual artifact for ABSOLUT Sport — the official CONMEBOL Libertadores™ & Sudamericana™ travel package agency, with offices in Rio de Janeiro, Frankfurt, Los Angeles and Buenos Aires. Triggers include landing pages, email templates, presentations, social media assets, ad creatives, voucher templates, marketing copy, decks, prompts for AI tools, internal documents and brand-aligned UI. Contains the canonical brandbook — colors (Azul ASB #155F97, Black #0D0D0D, Gold #C9A84C), typography (SoulCraft GX display + Barlow body + JetBrains Mono for data), 4 logo variants, Lucide iconography (2px stroke, geometric — never emoji), motion tokens, Mauricio voice rules, 4-language i18n (PT/EN/ES/DE), and 3 applied playbooks (AI Marketing, Enterprise AI, Growth). Co-authored by Mauricio Lacerda × Rafa Rafa. Suggestions to design@absolut-sport.com.br.
user-invocable: true
---

# ABSOLUT Sport · Brandbook Skill

This skill is the canonical brandbook for ABSOLUT Sport. When invoked, read `README.md` for the full context and use the rules below as guardrails.

## What's in this skill (file map)

| File | What it is | When to read |
|---|---|---|
| `README.md` | Brand overview, foundations, structure index | First, always |
| `colors_and_type.css` | All design tokens (colors, type, spacing, radius, motion) | Whenever generating CSS or referring to tokens |
| `I18N_METHOD.md` | Replicable translation method (i18n.js + dictionary pattern) | When working with multilingual content |
| `i18n.js` | Shared language toggle script (PT/EN/ES/DE) | Reference for new pages |
| `zero-to-o.js` | Brand signature: replaces "0" with "O" inside SoulCraft elements | Include in any page using SoulCraft |
| `index.html` | Live Hub of the design system | Reference for visual patterns |
| `playbooks/ai-marketing.html` | AI Marketing Playbook (live) | Reference for playbook structure |
| `playbooks/growth.html` | Growth Playbook (live) | Reference for playbook structure |
| `assets/` | 4 logo variants + brand kit zip | Use these, never recreate |
| `fonts/soulcraftgx.ttf` | SoulCraft GX (variable display font) | Bundle with new pages |
| `preview/` | 13 preview cards of components | Reference for component patterns |
| `ui_kits/website/` | React UI kit for absolut-sport.com.br | Reference for production patterns |

## Visual identity (canonical tokens)

### Colors

| Token | Value | Use |
|---|---|---|
| `--color-blue` | #155F97 | Primary — CTAs, accents, brand presence |
| `--color-blue-dark` | #0F4A75 | Hover state on primary |
| `--color-blue-mid` | #1E7ABE | Dark mode accent, lighter primary |
| `--color-black` | #0D0D0D | Authority, premium, dark backgrounds |
| `--color-off-white` | #FAFAFA | Default light background |
| `--color-gold` | #C9A84C | Authorship, "premium official", coauthor markers |
| `--color-gray-asb` | #C0C0C0 | Institutional gray, "inactive/secondary" elements |
| `--color-error` | #E3001B | **ONLY error states.** Never decorative. |

Full palette and neutrals in `colors_and_type.css`.

### Typography

| Family | Use | Token |
|---|---|---|
| `SoulCraft GX` | Headlines, marca, números grandes, brand display | `--font-display` |
| `Barlow` | UI, body, menus, forms | `--font-body` |
| `JetBrains Mono` | Data, prices, code, mono labels | `--font-mono` |

**Rules:**
- Brand headlines (Hero, Display, Headline) use SoulCraft. Always.
- SoulCraft is variable — use `font-weight: 900` + `font-variation-settings: 'wght' 900` for max impact.
- Include `zero-to-o.js` on any page using SoulCraft (signature: numbers like `+5oo`, `1oK`, `12o×`).

### Logos (4 variants)

| File | Use |
|---|---|
| `assets/logo-azul-preto.svg` | Primary · light backgrounds · institutional material |
| `assets/logo-azul-branco.svg` | Dark backgrounds · dark mode · night photography |
| `assets/logo-branco.svg` | Monochrome · blue or dark backgrounds · special applications |
| `assets/logo-preto.svg` | Monochrome · B&W print · light backgrounds · documents |

**Rules:**
- "ABSOLUT Sport" — always written in full. **Never just "Absolut".**
- Default for unknown context: Azul + Preto.
- Decision matrix at `index.html#decision`.

## Iconography (CRITICAL — non-negotiable)

**Lucide is the only sanctioned icon set.**

- 2px stroke
- Geometric, modern
- Inline SVG preferred (CDN is fragile)
- Catalog: https://lucide.dev

**ANTI-PATTERN — NEVER do this:**
- ❌ Emoji as icon (📦 📊 🎨 📣 🔍 ✉️ etc.) — they look ok in a draft, they break the system in production
- ❌ Custom drawn icons — breaks visual rhythm
- ❌ FontAwesome / Heroicons / other libraries — only Lucide

If tempted to use emoji because it's faster: stop. Use `<svg>` with the matching Lucide path. The catalog has equivalents for everything common.

## Motion (3 tokens)

| Token | Value | Use |
|---|---|---|
| `--transition-fast` | 0.15s ease-out | Hover, click, toggle — instant feedback |
| `--transition-default` | 0.20s ease-out | Cards, buttons, state change — standard |
| `--transition-slow` | 0.35s ease-out | Modal, drawer, content reveal — emphasis |

**Principles:**
- Motion is function, never decoration.
- Hover lifts 3px. Press drops 2px. Always `ease-out`.
- No springs / bounces. Controlled energy.
- Always wrap pages with `@media (prefers-reduced-motion: reduce)` global override.

## Voice and tone (Mauricio voice — PT canonical)

PT is canonical. EN/ES/DE adapt preserving rhythm, not literal translation.

### Rules

- Conclusion at the top, development below
- Active voice always ("eu fiz" — never "foi feito")
- Short and medium sentences alternating — never uniform paragraphs
- Aforismos when they fit (one-sentence diagnosis)
- "Carioca de café" register — professional but casual

### Banned words (PT)

complexo · multifacetado · jornada (exceto literal) · sinergia · mergulhar · holístico · alavancar (sentido vago) · impactar (verbo nobre) · robusto

### Banned words (EN)

delve · leverage · utilize · facilitate · streamline · harness · pivotal · seamless · cutting-edge · landscape (sector) · realm · tapestry · synergy · testament · innovative (vague) · robust · furthermore · moreover · consequently · thus · notably

### Canonical aforismos (already in production — quote, don't reinvent)

- "Lista de ideias não é plano." (Growth Playbook)
- "Quem não mede, supõe." (Growth Playbook)
- "AI é o nosso sexto jogador." (AI Playbook)
- "Tudo o que é bom, vem em dobro." (Banner Rafa Rafa)
- "Mostre, não descreva." (AI Playbook)
- "Sobe quem tem o lápis na mão." (GAL Process)
- "Seu julgamento é o produto." (Workflow AI)
- "Velocidade é o multiplicador. Repetição é a alavanca." (Growth Filosofia)
- "Growth é alavancagem iterativa." (Growth Hero)

### Brand taglines (do brandbook original)

- "Dos estádios para a história!" (primary)
- "ISSO É VIVER." (alt)
- "Eficiência alemã, entusiasmo brasileiro, estilo de vida californiano." (positioning)

## i18n (multilanguage)

Sistema baseado em `i18n.js` + dicionário inline por página.

**4 idiomas suportados:**

| Código | Mercado primário | Tom |
|---|---|---|
| `pt` | Rio · default canonical | Carioca informal |
| `en` | Los Angeles · global | International English |
| `es` | Buenos Aires · LATAM | Voseo argentino quando couber |
| `de` | Frankfurt | "Du" form (informal padrão) |

Método replicável documentado em `I18N_METHOD.md`. Padrões de marcação:
- `data-i18n="key"` — texto puro
- `data-i18n-html="key"` — texto com markup interno
- `data-i18n-attr="title:key"` — atributos

**Regra:** termos da marca (ABSOLUT Sport, CONMEBOL Libertadores™, Sudamericana™) e jargão técnico (Hero, Display, Tokens, AAARRR, ICE, ROAS) preservados em todos os idiomas.

## Playbooks aplicados (live)

3 playbooks ativos no Hub:

1. **AI Marketing** (`playbooks/ai-marketing.html`) — Como o time de marketing global usa AI no dia a dia. Use cases, regras, workflow e ferramentas.
2. **Enterprise AI Guide** (`higgsfield-ai-guide.html`) — Contas, segurança, boas práticas e arsenal de IA para times.
3. **Growth** (`playbooks/growth.html`) — Pilares (AAARRR), métricas, plataformas, metodologia, workflow, do/don't, glossário. Filosofia: "Alavancagem iterativa".

Cada playbook herda nav + footer + CSS do design system. Não criar playbook do zero — espelhar a estrutura desses 3.

## Light vs Dark mode (clarification)

`colors_and_type.css` define **light mode como canônico** nos tokens semânticos (`--bg-base: #FAFAFA`, `--fg-primary: #0D0D0D`).

**Mas as páginas publicadas (Hub, AI Playbook, Growth Playbook) usam dark mode** — porque ABSOLUT é "estádio à noite, dramatic, atletic". Dark mode reinforça o DNA visual.

**Regra prática:**
- Se o contexto pedir contraste com fotos noturnas, fundo dramático, energia de evento → **dark mode** (use `--color-black` como `bg`, `--color-white` como `fg`).
- Se for material institucional B2B, documentos formais, impressão → **light mode** (defaults canônicos do CSS).
- Quando em dúvida, espelhar o que está nas páginas publicadas: dark mode com `--color-blue` accent.

## Brand Toolkit (zip)

`assets/absolut-brand-kit.zip` — kit completo com 4 logos, SoulCraft GX, tokens.css, zero-to-o.js, README.

**Regenerar quando atualizar tokens/logos/fonte:**

```powershell
$base = "G:\Meu Drive\ABSOLUT Sport Design System"
Compress-Archive -Path $base\assets\logo-*.svg, $base\fonts\soulcraftgx.ttf, $base\colors_and_type.css, $base\zero-to-o.js, $base\README.md -DestinationPath $base\assets\absolut-brand-kit.zip -Force
```

## Anti-patterns (avoid these — they break the system)

| Anti-pattern | Por quê quebra | O certo |
|---|---|---|
| Emoji como ícone | Lucide é o set oficial — emoji quebra consistência visual | Lucide SVG inline (2px stroke) |
| Glassmorphism em cards de conteúdo principal | Dilui o DNA bold/atlético da ABSOLUT | Glassmorphism só em nav (HUD), modais, hover overlays |
| Opacity em estado disabled | Mata contraste, fere acessibilidade | Use `--color-gray-asb` (#C0C0C0) com texto escuro como tratamento "inativo" |
| Light mode em páginas públicas | Quebra o registro visual estabelecido | Use dark mode (preto + azul) por default |
| Hardcoded hex (`#155F97`) | Bypassa o sistema de tokens | Sempre `var(--color-blue)` |
| Tradução literal palavra-por-palavra | Mata o ritmo Mauricio | Adapte aforismos preservando peso, não palavras |
| Dois cores accent na mesma headline | Visualmente "tentando demais" — cara de IA | Uma cor accent por bloco |
| Múltiplos radial gradients sobrepostos no hero | Tropo de IA generativa, não DNA ABSOLUT | Diagonal gradient + barra accent vertical |
| `font-family` sem fallback | Quebra se SoulCraft falhar | Sempre `'SoulCraft', 'Barlow Condensed', sans-serif` |

## Authorship and contact

**Co-authored by Mauricio Lacerda × Rafa Rafa.**

- Mauricio Lacerda — Head of Marketing Americas
- Raphael Ferreira (Rafa Rafa) — Design Lead

Suggestions, change requests, doubts: **design@absolut-sport.com.br**

Crédito visível em:
- Header de toda página: badge gold "MM × RR" (top-right)
- Footer de toda página: linha "Criado por Mauricio Lacerda × Rafa Rafa · design@..."

## When this skill is invoked without specific guidance

Ask the user what they want to build or design. Then act as expert designer/copywriter who outputs:
- HTML artifacts (with full design system applied) for visual deliverables
- Production code (with tokens and patterns) for engineering tasks
- Mauricio voice copy in PT canonical (and adapt to EN/ES/DE if requested)

Default to dark mode unless the artifact is institutional/print/B2B formal.
