# Content Growth — Playbook do Blog ABSOLUT Sport

> **Playbook operacional do blog.** O braço *owned* do que a assessoria (Press FC) faz *earned*: a mesma pauta que ranqueia na Exame vira ativo próprio que ranqueia no Google, é citado por LLM e converte no produto Shopify. Deep-dive atrás do card "SEO / Conteúdo" do Growth Playbook.

- **Versão:** v1.0 · 23/jul/2026
- **Escopo:** loja BR (`absolut-sport.com.br`). US entra depois, mesma metodologia.
- **Fonte de estratégia (deep):** `keter/malkuth/absolut-sport-comunicacao/blog-br/plano-blog-absolut-sport-br.md`
- **Taxonomia (silos):** `cross-sell-taxonomy.md` — **fonte única, não redefinir aqui**
- **Metodologia:** Harahel (SEO técnico + AEO + Copy) + método Edward Sturm (GEO/LLM) + economia Hormozi
- **Relação com o Hub:** página filha `content-growth.html`; é o deep-dive do card "SEO / Conteúdo" (pilar Aquisição do AAARRR) do `growth.html`

---

## 1. Por que o blog (o quarto canal)

A descoberta hoje roda em três frentes desconectadas: produto Shopify (quem já busca), Press FC/earned (autoridade de marca), ads (tráfego alugado). Falta o canal de **menor CAC e maior retorno composto**: conteúdo *owned*. Só o blog ranqueia para quem ainda **pergunta**, é **citado por ChatGPT/Perplexity/AI Overview**, e captura o SEO que hoje evapora na URL do veículo.

Alimenta os dois motores de receita: **Flamengo** (recorrência/relacionamento) e **Libertadores** (volume/evento).

## 2. Owned × Earned

| | Earned (Press FC) | Owned (Blog) |
|---|---|---|
| Formato | Aspas do porta-voz em matéria de terceiro | Artigo próprio no domínio ABSOLUT |
| Ganho | Autoridade de marca + backlink | Ranking Google + citação LLM + CTA pro produto |
| Vida útil | Ciclo de notícia (dias) | Evergreen / renovável por temporada |

A citação na Exame vira backlink e sinal de autoridade de entidade (E-E-A-T) que turbina o AEO do blog; o blog vira a fonte estruturada que os LLMs referenciam.

## 3. Arquitetura Shopify (canônica, ADMIN baixo)

- **Um blog único** — objeto `Blog` nativo, handle `/blogs/revista`. Blog único concentra autoridade de domínio.
- **Tags = espelho da taxonomia comercial** (silo + evento). Ver `cross-sell-taxonomy.md`. Não recriar silos aqui.
- **Hub-and-spoke:** pillar = `Page` rica por evento âncora (`/pages/libertadores`); spokes = artigos linkando ↑ pillar e ↓ produto.
- **URL:** `/blogs/revista/{slug}` — keyword no slug, sem `#`, sem ID. Zero Liquid customizado.

## 4. Anatomia AEO do artigo (Harahel + Sturm)

- **Descoberta (query fan-out):** GSC regex 7+ palavras `(\b\w+\b\s){7,}` · queries do Perplexity · GA4 referral de IA (ChatGPT/Perplexity/Gemini).
- **On-page:** prompt-alvo em Title, Meta, slug, H1 e **início da 1ª frase**; título longo (~250 char); answer-first.
- **Citabilidade:** abertura ~150 palavras densa em entidades; blocos de **134–167 palavras** auto-suficientes; FAQ embutida.
- **Schema:** `Article` + `BreadcrumbList` + `FAQPage` + `SportsEvent` (evento datado) + `Product` (aponta pro produto). Sempre bate com o que o usuário vê.
- **Técnico:** crawl budget (não deixar bot ler filtros infinitos); frescor **real** > mudar data; reviews com evidência real (Alan Kent).
- **Timing (Google Trends):** publicar o cluster **antes do pico** (sorteio → oitavas → final).
- **Artifact-satélite (Sturm):** Claude Artifacts publicados ranqueiam em horas e são citados por Perplexity/AI Overviews — um por evento âncora.

## 5. Motor de produção

```
Pauta (Press FC / query fan-out / evento)
  → Rascunho Claude (voz Mauricio + copy Halbert/Brunson + oferta Hormozi)
  → GATE: revisão humana + evidência real (foto própria, dado, autoria)
  → Publish Shopify (Article + schema)
  → RSS → social → medir → loop A/B
```

**Regra inviolável (SpamBrain):** IA rascunha, **humano assina e adiciona evidência real** antes de publicar. Nunca conteúdo de IA em escala crua.

**Papéis:** Wictor (pillar/blocos/navegação) · Manoella (pós-venda/relacionamento — motor Flamengo) · Rodrigo Candido (foreman do que escala à Econverse). Cadência: SEO/AEO já é ritual semanal (diligência §3.3).

**Escala programmatic (estratégia "Zíper", Catliff):** cruzar dimensões de baixa concorrência — `hospitalidade {evento} {cidade}`, `pacote {timeA} x {timeB}`. Só publica célula com valor real; nunca thin content.

## 6. Auditoria de temas Press FC (jun–jul 2026)

Banco de pautas já validado (viraram matéria). **Escopo: auditoria do que existe**, não banco operacional.

| Silo | Pautas | Saiu em |
|---|---|---|
| Copa 2026 (dominante) | ocupação/6M · maior premiação · receita FIFA +42% · turismo global · camarote Atlanta R$2M · cerveja zero · uniforme R$382M · árbitros | Exame, CNN, Quem, Diario AS |
| Celebridades | Messi EUA · Endrick · Beckham · Ronaldinho/Bebeto/Zé Roberto | Diario AS, Leo Dias |
| Negócio | modelo europeu · seleção vs craque | Exame |
| Libertadores | "La Final de Todos" · ação Conmebol | em construção |
| Tênis | Wimbledon | em checagem |

**Veículos:** Exame · CNN · O Globo · Diario AS · Quem · Leo Dias · ESPN · A Bola · Ge.Globo · Itatiaia · Times Brasil · Correio Braziliense · Máquina do Esporte.

**Gap estratégico:** ~80% das pautas são Copa (marca/autoridade — topo/AEO), mas os motores de receita são Flamengo + Libertadores (conversão). Cada pauta de marca deve carregar link interno pro cluster comercial.

## 7. Economia do canal (Hormozi)

- **CAC ≈ 0** — orgânico + citação LLM não se paga por clique. Audiência que se possui, não se aluga.
- **LTGP:CAC → altíssimo** — a métrica-mãe da escala.
- **$100M Offer no CTA** (Value Ladder/Brunson); a "2ª venda" = motor Flamengo.
- **Balde furado (churn):** blog + relacionamento consertam o vazamento antes de jogar tráfego.

## 8. Linha ética (o que NÃO fazer)

Absorve o white-hat do Sturm (§4). Descarta o grey-hat: PR anônimo via Fiverr, reviews falsos, manipulação de Grok, compra de backlinks, thin content em massa. A ABSOLUT já tem a versão premium (Press FC real, evidência real, autoria real).

## 9. Roadmap

1. **Cluster #1 — Libertadores 2026** (piloto): pillar + 3–5 spokes AEO + Artifact-satélite.
2. **Cluster #2 — Flamengo evergreen**: guias de torcedor, "como funciona o pacote", pós-compra.
3. **Cluster #3 — Copa/celebridades**: reaproveita banco Press FC, sempre com link pro comercial.
4. **Camada programmatic "Zíper"** após piloto validado.
5. **Cadência:** N spokes/semana + 1 pillar por evento âncora.

## 10. Pendências

- [ ] Confirmar handle (`/blogs/revista`) e verificar blog legado no Shopify Admin.
- [ ] Criar dossiê canônico "Edward Sturm — AEO/GEO" (NotebookLM → Atzilut → sulam).
- [ ] i18n EN/ES/DE do `content-growth.html` (hoje PT canônico) — ver BACKLOG.
- [ ] Aprovar Cluster #1 (Libertadores) como piloto.

---

**Stack de conhecimento:** Harahel (skill) · dossiês SEO Google Search Central (NotebookLM: `b297c1fa`, `0176690f`, `8bbabdc6`, `e64387d0`, `05a466eb`) · Catliff/Claude Code SEO (`ab87a1ad`) · Halbert · Brunson · Hormozi (`92dfa1b4`, `cccc0bbb`) · Edward Sturm (edwardsturm.com).

*Co-autoria Mauricio Lacerda × Rafa Rafa · design@absolut-sport.com.br*
