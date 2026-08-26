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
- **Bold and aspirational** — copy is written with emotional charge ("experiências lendárias", "momentos inesquecíveis")
- **Authoritative** — references to official status and credentials ("Única Agência Oficial")
- **Warm but premium** — not cold luxury; passionate Brazilian energy with German precision
- **Second person (você)** — brand speaks directly to the customer
- **Exclamation heavy** — enthusiasm is part of the brand voice
- **Capitalized proper nouns** — CONMEBOL, ABSOLUT Sport, etc. always styled in caps/title case

### Casing
- Brand name: **ABSOLUT Sport** (ABSOLUT in caps, Sport in title case)
- Headlines: ALL CAPS or Title Case for major calls to action
- Body: Sentence case
- Taglines: ALL CAPS ("DOS ESTÁDIOS PARA A HISTÓRIA", "ISSO É VIVER")

### Copy Examples
- "Somos a única agência oficial de pacotes para as Finais da CONMEBOL Libertadores™"
- "Experiências esportivas lendárias"
- "Vivências imersivas e emocionantes que transcendem o jogo"
- "Excelência, conforto e segurança"
- "O céu é o limite para que você viva experiências lendárias!"
- "Eficiência alemã, entusiasmo brasileiro e estilo de vida californiano"

### Emoji Usage
- Used sparingly in social media contexts (🤝 for partnerships)
- NOT used in primary website UI or marketing materials

---

## VISUAL FOUNDATIONS

### Color System
- **Primary Blue:** `#155F97` — Azul ASB, cor institucional primária, CTAs e destaques
- **Blue Dark:** `#0F4A75` — hover states, profundidade
- **Blue Mid:** `#1E7ABE` — versão dark mode do azul primário
- **Blue Highlight:** `#2857F7` — acento de destaque, hover emphasis
- **Black:** `#0D0D0D` — background escuro, autoridade, premium
- **White:** `#FFFFFF` — texto em fundos escuros, superfícies limpas
- **Off-White:** `#FAFAFA` — background padrão light mode (modo primário)
- **Gray ASB:** `#C0C0C0` — cinza institucional, elementos secundários
- **Gold/Amber:** `#C9A84C` — tier premium, badges VIP, "oficial"
- **Error/Alert:** `#E3001B` — somente estados de erro e alertas críticos

### Logo
- Mark: A stylized bold capital **"A"** (no crossbar) — monolithic, modern
- Red oval accent top-right of the "A" — like a ball or badge
- Wordmark: "Absolut" in bold uppercase sans-serif below the mark
- Color: Black on light backgrounds; White on dark; Red accent always preserved
- Usage: "ABSOLUT Sport" — never just "Absolut"

### Typography
- **Display / Headlines:** SoulCraft GX (variable, weight 900 para impacto máximo) — tipografia primária da marca, alta voltagem
  - Fonte local: `fonts/soulcraftgx.ttf` (incluída no `absolut-brand-kit.zip`)
  - Fallback: Barlow Condensed, sans-serif
  - Assinatura: incluir `zero-to-o.js` em qualquer página com SoulCraft (troca "0" por "O" maiúsculo — `+5oo`, `1oK`, `12o×`)
- **Body / UI:** Barlow (Regular/Medium/SemiBold) — clean, readable, modern
  - Fallback: DM Sans, Inter
  - Google Fonts (gratuito, livre): https://fonts.google.com/specimen/Barlow
  - Display fallback (gratuito): https://fonts.google.com/specimen/Barlow+Condensed
- **Mono / Data:** JetBrains Mono — for prices, codes, stats
  - Google Fonts (gratuito): https://fonts.google.com/specimen/JetBrains+Mono

> **Acesso às fontes:** SoulCraft GX está empacotada no `assets/absolut-brand-kit.zip` (download via Hub). Barlow e JetBrains Mono são gratuitas no Google Fonts — qualquer pessoa com acesso ao Hub pode baixá-las nos links acima.

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
- `assets/logo-azul-preto.svg` — **Primária** · Logo Azul + Preto · fundos claros (light mode)
- `assets/logo-azul-branco.svg` — Logo Azul + Branco · fundos escuros (dark mode)
- `assets/logo-branco.svg` — Logo Branco monocromático · fundos azuis ou escuros
- `assets/logo-preto.svg` — Logo Preto monocromático · impressão P&B · fundos claros

---

## SKILL INDEX

| File | Description |
|------|-------------|
| `index.html` | **Design System Hub** — página pública para a empresa toda. Logos, cores, tipografia, tokens, componentes, guidelines e devs. Publicar em subdomínio (ex: `design.absolut-sport.com.br`). |
| `playbooks/ai-marketing.html` | **AI Marketing Playbook** — página filha do Hub, voltada ao time de marketing global. |
| `playbooks/content-growth.html` | **Content Growth Playbook** — página filha do Hub. O blog owned: arquitetura Shopify, anatomia AEO, motor de produção, auditoria de pautas da assessoria e economia do canal (Hormozi). Deep-dive atrás do card "SEO / Conteúdo" do Growth. PT canônico (i18n EN/ES/DE = BL-006). |
| `playbooks/content-growth.md` | **Content Growth · CANÔNICO (playbook doc)** — versão texto do playbook do blog. Referencia `cross-sell-taxonomy.md` (silos) e a estratégia deep no vault. Padrão da suíte de taxonomia. |
| `playbooks/` | Pasta para playbooks aplicados (cada um é uma página filha do Hub). |
| `email-command-center.html` | **Email Marketing · Command Center** — dashboard interno do projeto de email marketing. 10 abas (Visão Geral · Master Strategy · 6 silos legados · Tracking · Templates). ⚠ Em migração para nova taxonomia (7 silos + 2 programas, 3 níveis silo/sub-silo/evento) — ver `playbooks/cross-sell-taxonomy.md` e `playbooks/growth-email.html`. Brandbook ABSOLUT aplicado: tokens, SoulCraft, Lucide. Ferramenta operacional do time de Growth. |
| `playbooks/cross-sell-taxonomy.md` | **Cross-Sell Taxonomy · CANÔNICO** — modelo canônico de taxonomia em 3 níveis (silo → sub-silo → evento), matriz de afinidade entre sub-silos, regras de gatilho para automação RD Station. Versão 1.0 · maio/2026. |
| `playbooks/cross-sell-matrix.csv` | **Matriz de afinidade · 169 pares** — origem/destino/score em formato long. Pronto pra Victor importar no RD Station. Acompanha o canônico. |
| `playbooks/taxonomy-takeaway.md` | **Takeaway 1 página · Para Daniel + stakeholders** — explicação sem jargão da nova taxonomia: o que mudou, por que mudou, o que não mudou. Leitura de 3 minutos. |
| `playbooks/taxonomy-quick-reference.md` | **Quick Reference · Para Jack, Rachella, Victor, Wictor** — cartão de bolso: os 3 níveis, os 7 silos, as 8 perguntas antes de escrever email, matriz cross-sell condensada, frontmatter padrão. Imprime e cola na mesa. |
| `playbooks/taxonomy-folder-template.md` | **Template de pastas · Para Wictor + Drive** — estrutura física completa do Drive seguindo a taxonomia. Inclui checklists para criar novo evento, sub-silo ou silo. Princípios não-negociáveis. |
| `playbooks/copy-library.html` | **Copy Library · Aby — Biblioteca de Respostas Rápidas** — 35 mensagens em 13 categorias com sistema de variáveis para reuso por evento. Filtro por categoria, busca, copy-to-clipboard, i18n PT/EN/ES/DE. Página viva alimentada por JSONs gerados via `playbooks/copy-library/extract.py`. Fonte: planilha canônica (gid 1469143387). |
| `playbooks/copy-library/` | Dados estruturados e script gerador: `extract.py` (interpretador da planilha), `input.tsv` (fonte), `messages.json` + `variables.json` (dados), `i18n-{pt,en,es,de}.json` (dicionários). Ver `playbooks/copy-library/README.md`. |
| `README.md` | Este arquivo — visão da marca, fundamentos, índice. |
| `colors_and_type.css` | CSS custom properties para todos os design tokens. **Importar nas páginas via `<link>`.** |
| `zero-to-o.js` | Script que troca "0" por "O" maiúsculo em texto SoulCraft (assinatura da marca). Incluir em qualquer página com SoulCraft. |
| `fonts/soulcraftgx.ttf` | Fonte de display SoulCraft GX. |
| `preview/` | Preview cards de cada componente (linkados do Hub). |
| `assets/` | Logos e brand assets (.svg). |
| `assets/absolut-brand-kit.zip` | **Brand Kit completo** — 4 logos + SoulCraft GX + colors_and_type.css + zero-to-o.js + README. Linkado no Hub via CTA "Brand Kit". Regenerar via PowerShell `Compress-Archive` quando atualizar tokens/logos/fonte. |
| `assets/rafa-rafa.png` | Cartaz do banner "Pergunte pro Rafa" no rodapé do Hub. Também usado como `og:image` em todas as páginas. |
| `assets/mauricio.jpg` | _TODO_: foto do Mauricio Lacerda. Reservada para uso planejado (banner de coautoria, perfil de coordenação, ou expansão do banner Rafa Rafa pra dupla). Mantida no repo até a decisão de uso. |
| `ui_kits/website/` | UI kit React para absolut-sport.com.br. |
| `SKILL.md` | **Brandbook Skill (Claude)** — spec completa do brandbook em formato Claude skill. Carrega regras de cor, tipografia, ícones (Lucide), motion, voz Mauricio, i18n, playbooks aplicados, anti-padrões e contato. Veja seção "Skill Claude" abaixo pra ativar localmente. |
| `I18N_METHOD.md` | Método replicável de tradução (i18n.js + dicionário inline). Pra usar o mesmo padrão em outros projetos. |

---

## SKILL CLAUDE · BRANDBOOK

`SKILL.md` é o canon do brandbook em formato Claude skill. Quando ativada, carrega contexto completo: cores, tipografia, logos, regras de iconografia (Lucide), motion, voz Mauricio, i18n nos 4 idiomas, playbooks aplicados e anti-padrões.

### Pra que serve

Qualquer Claude (Code, Desktop, API) com a skill ativada vai gerar artefatos visuais e textuais já alinhados ao brandbook ABSOLUT Sport — sem precisar repetir as regras a cada conversa. Cobre:

- Landing pages, e-mails, decks, social media
- Copy em PT/EN/ES/DE com voz Mauricio
- HTML production-ready com tokens e componentes do design system
- Prompts pra ferramentas AI (Midjourney, ChatGPT, etc.) já formatados com contexto da marca

### Ativar localmente (Claude Code)

Copiar a pasta inteira pro diretório de skills do Claude Code:

```powershell
$src = "G:\Meu Drive\ABSOLUT Sport Design System"
$dest = "$env:USERPROFILE\.claude\skills\absolut-sport-design"
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Copy-Item -Path $src -Destination $dest -Recurse
```

A skill é descoberta automaticamente via `SKILL.md`. Ativar via `/skills` no Claude Code, ou invocar diretamente em conversa quando precisar.

### Atualizar a skill

Mudou alguma coisa no design system (token novo, aforismo novo, anti-padrão a documentar)? Edite o `SKILL.md` na raiz do projeto. Re-rode o `Copy-Item` acima pra propagar.

Quando o subdomínio `design.absolut-sport.com.br` estiver no ar, a skill vai poder ser instalada via download direto do `SKILL.md` + arquivos referenciados.

### Triggers de uso (quando a skill se ativa)

A `description` no frontmatter inclui keywords que disparam a skill quando relevante:
- "ABSOLUT Sport", "CONMEBOL Libertadores", "Sudamericana"
- "landing page", "email template", "deck", "social media", "voucher"
- "marketing copy", "brand colors", "logo"
- "Mauricio", "Rafa Rafa", "design@absolut-sport.com.br"

---

## DEPLOY — Como publicar

O Hub é uma página estática, sem build, sem servidor de aplicação.

### Onde fica o quê

- **URL canônica:** `https://design.absolut-sport.com.br` (subdomínio próprio)
- **Embed:** `https://absolut-sport.com.br/pages/design-system` (Shopify, iframe do subdomínio)
- **Email de contato:** `design@absolut-sport.com.br` (sugestões, alterações, dúvidas)

### Passos de publicação

1. **Host estático** — recomendado **Cloudflare Pages** (grátis, drop-and-deploy, HTTPS automático). Alternativa: Netlify (`https://app.netlify.com/drop`).
2. **Subir a pasta inteira** — `index.html` é o ponto de entrada. Caminhos são todos relativos (`./assets/...`, `./fonts/...`, `./preview/...`).
3. **DNS** — criar CNAME `design` apontando para o subdomínio `pages.dev` (ou equivalente).
4. **SSL** provisiona em ~5–15 min. Testar em aba anônima.

### Embed no Shopify

No Shopify admin → Pages → criar nova página com handle `design-system`. Conteúdo (HTML view):

```html
<iframe
  src="https://design.absolut-sport.com.br"
  title="ABSOLUT Sport Design System"
  loading="lazy"
  style="display:block;width:100%;height:calc(100vh - 120px);border:none;"
  allow="clipboard-write"
></iframe>
```

Se o iframe não carregar, ajustar Cloudflare Pages → Settings → Headers:
```
Content-Security-Policy: frame-ancestors 'self' https://absolut-sport.com.br https://*.absolut-sport.com.br;
```

### Coautoria e contato

O design system é **co-autoria de Mauricio Lacerda × Raphael Ferreira (Rafa Rafa)**. Crédito visível no header (badge gold "MM × RR") e no rodapé de toda página. Qualquer alteração, sugestão ou solicitação: `design@absolut-sport.com.br`.

### Acesso

Link público — qualquer pessoa com a URL acessa. Brand guidelines são distribuídas livremente entre os 4 escritórios (Rio, Frankfurt, LA, Buenos Aires).

### Idiomas suportados

Toggle no canto superior direito de toda página. Preferência persiste em `localStorage` (`asb_lang`).

| Código | Idioma | Mercado primário |
|---|---|---|
| `pt` | Português (BR) | Rio de Janeiro · default |
| `en` | English | Los Angeles · global |
| `es` | Español | Buenos Aires · LATAM |
| `de` | Deutsch | Frankfurt |

---

## ESTRUTURA HIERÁRQUICA

```
ABSOLUT Sport Design System/
├── index.html                       ← Hub principal (público)
├── colors_and_type.css              ← Tokens canônicos (importar)
├── zero-to-o.js                     ← Assinatura tipográfica
├── README.md                        ← Este arquivo
├── playbooks/
│   └── ai-marketing.html            ← AI Playbook (Marketing Global)
├── preview/                         ← 13 preview cards de componentes
├── ui_kits/website/                 ← UI kit React do site público
├── assets/                          ← 4 variantes de logo (.svg)
└── fonts/                           ← SoulCraft GX
```
