# Brand Guide Overhaul — Brief de Hand-off

> Documento de transferência. Use como prompt inicial / contexto na pasta correta.
> Captura: o que foi acordado, o que existe hoje no artefato, e o plano de ataque.

---

## 1. Decisões já tomadas com o usuário

| Pergunta | Resposta |
|---|---|
| Qual artefato aprimorar? | `index.html` do design system (Hub principal) |
| Onde está o "genérico" mais crítico? | **Cor e tipografia sem narrativa** — cards de cor e specimens de tipo parecem template, não mostram aplicação real |
| Direção de referência | **Rapanui (marca argentina)** — não a paleta nem a estética visual, mas o **DNA narrativo**: cada peça tem origem, história, contexto, hand-feel |
| Escopo | **Overhaul completo** — reestruturar todas as seções, adicionar capítulos novos, tratar como brand book completo |
| Onde cor/tipo precisam aparecer aplicadas? | **Brand in Use** — capítulo dedicado com 3 mockups: ingresso/voucher Libertadores, card social, hero de página de produto |

---

## 2. Tradução do "DNA Rapanui" para a ABSOLUT Sport

A Rapanui (clothing argentina) NÃO entra como referência estética (paleta terra/Patagônia não combina com o azul institucional ABSOLUT). Entra como **modo de apresentação**:

**O que Rapanui faz bem (e que o guide ABSOLUT precisa adotar):**
- Cada produto tem uma *story* — origem, inspiração, técnica, onde foi feito
- Mostra o produto **em uso** (vestido, no contexto), nunca isolado num grid
- Hand-feel: anotações, sketches, "behind the scenes", linguagem em primeira pessoa
- Cada cor/estampa carrega um significado declarado (fauna, paisagem, momento)

**Aplicação no brand book ABSOLUT:**
- Cada cor vem com: nome → emoção → onde aparece → exemplo real (mockup, não swatch)
- Cada peso tipográfico vem com: função no estádio → exemplo (placar, headline de jornal, manchete de pacote)
- Sidebar "field notes" estilo caderno do designer ao lado das specs frias
- Microcopy em primeira pessoa do time ("a gente usa essa em..."), não institucional

---

## 3. Estado atual do `index.html` (mapa do que existe)

**Arquivo:** 2314 linhas, totalmente self-contained (CSS inline + JS inline + i18n em 4 idiomas).

**Seções na ordem atual:**
1. `splash` — loading 2.5s com logo + linha azul
2. `nav` — sticky, glassmorphism, lang toggle (PT/EN/ES/DE), credit "MM × RR"
3. `#top` (hero) — eyebrow + h1 com 3 linhas + sub + cidades
4. `#toolkit` — CTA gold pra baixar zip do brand kit
5. `#logos` — 4 cards (Azul+Preto, Azul+Branco, Branco mono, Preto mono)
6. `#decision` — matriz 2×2 de quando usar cada logo
7. `#cores` — 3 grids (Brand Core, Neutrais, Status) renderizados via JS, click pra copiar hex
8. `#tipografia` — type-stack com 5 specimens (Hero/Display/Headline/Title/Body)
9. `#iconografia` — grid de 12 ícones Lucide inline
10. `#motion` — 3 cards de transição (fast/default/slow) + lista de princípios
11. `#tokens` — spacing list (12 valores) + radius cards (5 valores)
12. `#componentes` — grid de 13 component previews (links pra `preview/*.html`)
13. `#figma` — 4 cards de templates Figma externos
14. `#guidelines` — 6 blocos do/don't (Voz, Foto, Tipografia)
15. `#devs` — 3 snippets de código pra implementação
16. `#playbooks` — 2 cards ativos + 1 "coming soon" Growth
17. `ask-rafa-section` — banner gold com pôster do Rafa Rafa
18. `footer` — 3 colunas + bottom bar

**Sistema técnico:**
- `colors_and_type.css` — todos os tokens canônicos (cores, type, spacing, radius, shadows, transitions, z-index)
- `i18n.js` — toggle de idioma, persiste em `localStorage.asb_lang`
- `zero-to-o.js` — assinatura tipográfica (troca "0" por "O" maiúsculo em SoulCraft)
- `assets/` — 4 logos SVG + brand kit zip + foto Rafa
- `fonts/soulcraftgx.ttf` — fonte de display variable
- `preview/` — 13 component previews
- `playbooks/` — playbooks aplicados

**Restrições importantes:**
- Tokens em `colors_and_type.css` são canônicos — **não alterar**, apenas consumir
- i18n: qualquer key nova precisa de tradução em **PT, EN, ES, DE** dentro do `window.I18N_DICT`
- Padrão `data-i18n="key"` ou `data-i18n-html="key"` no DOM
- Caminhos relativos (sem build) — funciona em GitHub Pages / Cloudflare Pages
- WCAG AA já está validado para os pares de contraste atuais

---

## 4. Plano de overhaul proposto (chaptered brand book)

Reestruturar o Hub como **brand book com capítulos numerados**, abandonando a estrutura linear de "Hub-com-grids":

```
INTRO        → Hero novo + manifesto curto + sumário visual
CAP 01       Identidade
              ├─ 01.1 Anatomia do logo (NOVO — diagrama anotado)
              ├─ 01.2 Variantes oficiais (logos atual)
              └─ 01.3 Decisão (matriz atual, polida)
CAP 02       Cor — narrativa primeiro
              ├─ 02.1 A história da paleta (eyebrow narrativo)
              ├─ 02.2 Brand Core com contexto (cada cor: emoção + uso real)
              ├─ 02.3 Neutrais (escala fria)
              └─ 02.4 Status
CAP 03       Tipografia — em ação
              ├─ 03.1 As 3 vozes (SoulCraft, Barlow, JetBrains Mono — por que cada uma)
              ├─ 03.2 Especímenes em contexto (placar, manchete, ingresso)
              └─ 03.3 Hierarquia (waterfall atual, polido)
CAP 04       Brand in Use ★ (NOVO — entrega central do overhaul)
              ├─ 04.1 Mockup: Voucher / Ingresso Libertadores
              ├─ 04.2 Mockup: Card social (Instagram post)
              └─ 04.3 Mockup: Hero de página de produto
CAP 05       Voice & Tone aplicado (NOVO — substitui guideline genérico)
              ├─ 05.1 Os 3 sotaques (alemão · brasileiro · californiano)
              ├─ 05.2 Exemplos PT/EN/ES lado a lado
              └─ 05.3 Microcopy em situações reais (CTA, erro, vazio, sucesso)
CAP 06       Sistema (specs frias)
              ├─ 06.1 Iconografia
              ├─ 06.2 Motion
              ├─ 06.3 Tokens (spacing + radius)
              └─ 06.4 Componentes (preview grid)
CAP 07       Implementação
              ├─ 07.1 Para devs (snippets atuais)
              ├─ 07.2 Para designers (Figma templates)
              └─ 07.3 Brand kit download
APÊNDICE     Playbooks + Ask Rafa + Footer
```

**Mudanças visuais transversais:**
- Capítulo abre com **número grande** (ex: "01 — IDENTIDADE") em SoulCraft Black gigante
- Cada capítulo tem cor de borda/eyebrow distinta (mas dentro da paleta) pra criar ritmo
- Layout deixa de ser sempre "eyebrow → title → grid" — varia entre full-bleed, asymmetric, split
- "Field notes" sidebar (estilo caderno, monospace, em algumas seções)
- Microcopy em primeira pessoa do time, não institucional

---

## 5. Mockups "Brand in Use" — especificação dos 3 entregáveis

Tudo em SVG inline ou CSS puro (sem dependência de imagem real, já que não temos foto de stadium licenciada).

### 5.1 Voucher / Ingresso Libertadores
- Estádio noturno (ilustração CSS gradient, não foto)
- Logo Azul+Branco no topo
- Headline: "FINAL CONMEBOL LIBERTADORES™ 2026"
- Sub: "Estadio Maracanã · 30.NOV.2026"
- Stat strip: assento, setor, portão (Barlow + JetBrains Mono)
- Badge VIP gold no canto
- QR placeholder
- **Mostra:** Azul Dark de fundo, Gold pra VIP, Branco pra texto, JetBrains Mono pra dados

### 5.2 Card social (Instagram post 4:5)
- Foto de fundo (placeholder gradient + grain)
- Headline SoulCraft "DOS ESTÁDIOS PARA A HISTÓRIA"
- Sub Barlow "Pacotes Libertadores 2026 · A partir de"
- Preço em JetBrains Mono enorme
- CTA red "COMPRAR PACOTE"
- Logo branco no topo
- **Mostra:** hierarquia tipográfica completa em peça real, vermelho como CTA único

### 5.3 Hero de página de produto
- Layout split 60/40
- Esquerda: foto full-bleed (gradient placeholder)
- Direita: card flutuante com pacote (cidade, datas, hotel, preço, CTA)
- Eyebrow azul "OFICIAL · CONMEBOL™"
- **Mostra:** off-white card sobre dark, blue-mid pra eyebrow, gold pra "Oficial", red pra CTA

---

## 6. Anatomia do Logo (capítulo novo)

Diagrama anotado em SVG do logo Azul+Preto, com legendas:
- **Mark "A"** — monolítica, sem travessão (modernidade, autoridade)
- **Acento oval superior direito** — bola/troféu (emoção esportiva)
- **Wordmark** — sempre "ABSOLUT Sport" completo (nunca só "Absolut")
- **Espaço de respiro** — 1× a altura do mark em todos os lados
- **Tamanhos mínimos** — digital 24px alt, impresso 12mm alt
- **Don'ts visuais** — esticar, mudar cor da bola, separar mark do wordmark, aplicar sombra

---

## 7. Próximos passos recomendados (na pasta certa)

1. Confirmar caminho/repositório correto e branch de trabalho
2. Validar este plano (especialmente a estrutura de capítulos) antes de codar
3. Começar por **um único capítulo de prova** (sugiro Cap 02 Cor com narrativa + Cap 04.1 Voucher) pra validar a direção visual antes de aplicar nas 17 seções
4. Só depois de o usuário aprovar o "vibe check", reescrever o resto
5. Manter `colors_and_type.css` intocado, manter compatibilidade com `i18n.js`, atualizar i18n dict pra todas keys novas em PT/EN/ES/DE
6. Commit em `claude/improve-brand-guide-design-XXX` (ou branch designada na pasta correta)

---

## 8. Avisos de sanidade

- O Hub atual já é sofisticado (splash, glassmorphism, motion, i18n 4 idiomas, WCAG validado). Não tratar como blank slate. Reestruturar narrativa, mas preservar engenharia.
- Tokens em `colors_and_type.css` foram cuidadosamente validados (contrastes WCAG AA). Não mexer.
- `zero-to-o.js` é assinatura de marca — manter ativo em qualquer headline SoulCraft que tenha "0".
- Co-autoria Mauricio × Rafa Rafa precisa continuar visível (nav credit + footer + Ask Rafa banner).
- O tom do Ask Rafa banner ("Tudo o que é bom vem em dobro") é um padrão de microcopy que define a voz — não cortar.
