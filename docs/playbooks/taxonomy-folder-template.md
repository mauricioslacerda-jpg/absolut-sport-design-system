# Template de Pastas — Taxonomia ABSOLUT

> Como organizar fisicamente um silo/sub-silo/evento no Google Drive.
> Versão 1.0 · 2026-05-14 · Wictor + qualquer um que crie novo evento

---

## Estrutura completa (root)

```
/ABSOLUT-Sport-Operacao/
   /00-Taxonomia/                              ← single source of truth
      cross-sell-taxonomy.md                   (cópia do canônico)
      cross-sell-matrix.csv                    (matriz 169 pares)
      taxonomy-quick-reference.md              (cartão de bolso)
      publicos-definicao.md                    (B2C, B2B, B2B2C, HNWI)
      schwartz-decision-tree.md                (qual hook em cada quadrante)

   /01-American-Sports/                        ← Silo
      /NFL/                                    ← Sub-silo
         /Super-Bowl-LXI/                      ← Evento
         /Super-Bowl-LXII/                     ← próxima edição
         /NFL-International-Series-2026/
         /NFL-Regular-Season-2026/
         /NFL-Playoffs-2026/
      /NBA/
         /NBA-Regular-Season-2026-27/
         /NBA-Finals-2026/
         /NBA-All-Star-2027/
      /Golf/
         /Masters-Augusta-2026/
         /PGA-Championship-2026/
         /US-Open-Golf-2026/
         /The-Open-Championship-2026/

   /02-Futebol/
      /Libertadores/
         /Libertadores-2026/
         /Final-Libertadores-2026/
      /Sudamericana/
      /Recopa/
      /Flamengo/
         /Flamengo-Brasileirao-2026/
         /Flamengo-Maracana-experiencias/
      /Copa-do-Mundo/
         /Copa-do-Mundo-2026-Norte-America/
      /Brasileiro/
      /Europeu/
         /Champions-League-2025-26/
         /Premier-League-experiencias/

   /03-Automobilismo/
      /F1-SP/
         /F1-GP-Sao-Paulo-2026/                (8 nov 2026)
      /F1-Global/
         /Australia-Melbourne-2026/            (8 mar)
         /China-Xangai-2026/                   (15 mar)
         /Japao-Suzuka-2026/                   (29 mar)
         /Miami-2026/                          (3 mai)
         /Canada-Montreal-2026/                (24 mai)
         /Monaco-2026/                         (7 jun)
         /Espanha-Barcelona-2026/              (14 jun)
         /Austria-Spielberg-2026/              (28 jun)
         /UK-Silverstone-2026/                 (5 jul)
         /Belgica-Spa-2026/                    (19 jul)
         /Hungria-Hungaroring-2026/            (26 jul)
         /Holanda-Zandvoort-2026/              (23 ago)
         /Italia-Monza-2026/                   (6 set)
         /Espanha-Madrid-Madring-2026/         (13 set)
         /Azerbaijao-Baku-2026/                (26 set)
         /Singapura-2026/                      (11 out)
         /EUA-Austin-COTA-2026/                (25 out)
         /Mexico-Cidade-do-Mexico-2026/        (1 nov)
         /Las-Vegas-2026/                      (21 nov)
         /Catar-Lusail-2026/                   (29 nov)
         /Abu-Dhabi-Yas-Marina-2026/           (6 dez)
      /MotoGP-Goiania/
         /MotoGP-Brasil-Goiania-2026/          (20-22 mar 2026)
      /MotoGP-Global/                          (pré-mapeamento Fase 2)

   /04-Esportes-Olimpicos/                     (Fase 2 · em mapeamento)
      /Atletismo/
      /Canoagem/
      /Ginastica/
      /Volei/
      /Handball/

   /05-Tenis/
      /Grand-Slams/
         /Australian-Open-2026/                (jan 2026)
         /Roland-Garros-2026/                  (mai-jun 2026)
         /Wimbledon-2026/                      (jun-jul 2026)
         /US-Open-2026/                        (ago-set 2026)
      /NFTO-Brasil/
         /NFTO-Sao-Paulo-2026/

   /06-Promocionais-ASB/
      /Brand-Storytelling/
      /Bastidores/
      /Posicionamento/
      /Relacionamento-de-base/

   /07-Oportunidades-Calendario/
      /2026-Q1/
      /2026-Q2/
      /2026-Q3/
      /2026-Q4/
      /Black-Friday-2026/
      /Cyber-Week-2026/
      /Newsjacking-Reativo/

   /Prog-01-ABSOLUT-Pass/
      /Onboarding/
      /Renovacao/
      /Upgrade/
      /Win-back/

   /Prog-02-Cross-sell/                        (governança apenas; copy real vive em /05-cross-sell/ de cada evento)
      /Campanhas-multi-silo/
      /Sequencias-aniversario/
      /Win-back/
```

---

## Estrutura interna de cada **evento**

Dentro de cada pasta de evento (ex: `Super-Bowl-LXI/`), sempre as mesmas 6 subpastas:

```
/{evento}/
   00-briefing/                    ← FATO do evento. 1 lugar único.
      evento.md                    (data, local, capacidade, hotel, transfer)
      pacotes.md                   (Signature, Prestige, Pinnacle — o que inclui, preço)
      fornecedores.md              (ManyChat, RD Station, hotel, transfer, agências)
      calendario-fases.md          (Fase 1 a 9 da campanha)
      contato-clientes.md          (Jack, Rachella, suporte direto)

   01-leads/                       ← BASE de leads. 1 lugar único.
      lista-master.csv             (todos os leads com coluna "publico": B2C/B2B/B2B2C/HNWI)
      segmentacoes/                (queries salvas por público + por afinidade cross-sell)
      planilha-asana-link.md       (link pra planilha viva no Asana, se houver)

   02-copy/                        ← COPY. Divide por público AQUI.
      /b2c/
         email-01-boas-vindas.md
         email-02-storytelling.md
         email-03-urgencia.md
         email-04-prova-social.md
      /b2b/
         email-01-proposta.md
         email-02-roi-case.md
         email-03-fechamento.md
      /b2b2c/
         email-01-parceria.md
         email-02-cobranding.md
      /hnwi/
         email-01-acesso-curado.md
         email-02-private-dinner.md
         email-03-curadoria-pessoal.md

   03-assets/                      ← Imagens, vídeos, logos. 1 lugar único.
      fotos-oficiais/
      videos-edicoes-anteriores/
      logos/
      mockups/

   04-execucao/                    ← Histórico de envios.
      enviados/
         2026-01-15-welcome-b2c.md
         2026-01-20-proposta-b2b.md
      retro/
         retro-fase-2.md

   05-cross-sell/                  ← Emails de saída pra OUTROS silos.
      /para-f1-sp/
         email-01-teaser.md
         email-02-case.md
         email-03-abertura.md
      /para-grand-slams-us-open/
      /para-nfl-int-series/
```

---

## Quando criar um novo evento — checklist

1. ☐ Identifique o silo e sub-silo corretos (consultar Quick Reference)
2. ☐ Crie a pasta do evento com nome `{Modalidade-Local-Ano}` (kebab-case, ano explícito)
3. ☐ Copie a estrutura interna padrão (6 subpastas: `00-briefing/` a `05-cross-sell/`)
4. ☐ Preencha `00-briefing/evento.md` com data, local, capacidade, hotel
5. ☐ Atribua público dominante e público secundário (decide quais subpastas em `02-copy/` ativar)
6. ☐ Registre o evento em `00-Taxonomia/cross-sell-matrix.csv` se houver override por evento
7. ☐ Crie automação no RD Station seguindo regras de gatilho da `cross-sell-taxonomy.md` §4
8. ☐ Avise o time no canal #email-growth para sincronizar

---

## Quando criar um novo **sub-silo** (modalidade nova)

Ex: a ABSOLUT decide entrar em **Surf** (WSL Saquarema).

1. ☐ Decidir o silo-pai. Surf provavelmente entra em **04-Esportes-Olímpicos** (foi olímpico em Tóquio/Paris) ou cria um novo silo (Esportes Aquáticos).
2. ☐ Discutir com Mauricio antes de criar silo novo. Sub-silo novo dentro de silo existente é mais barato e quase sempre suficiente.
3. ☐ Criar pasta `04-Esportes-Olimpicos/Surf/`.
4. ☐ Adicionar linha + coluna em `cross-sell-matrix.csv` com afinidades para os 13 sub-silos existentes (consultar Mauricio).
5. ☐ Atualizar `cross-sell-taxonomy.md` §3 (matriz) + `taxonomy-quick-reference.md` (tabela).
6. ☐ Atualizar `growth-email.html` (card visual) + `email-command-center.html` (quando BL-005 estiver pronto).
7. ☐ Atualizar este documento (lista no root acima).

---

## Quando criar um **silo** novo (categoria nova)

**Raramente.** Os 7 silos atuais cobrem >95% das oportunidades comerciais previsíveis. Antes de criar:

1. ☐ Tente encaixar como sub-silo num silo existente.
2. ☐ Se realmente não cabe, abrir discussão com Mauricio + Daniel.
3. ☐ Se aprovado, novo silo recebe número sequencial (Cat. 08, Cat. 09…). **Nunca renumerar os existentes.**
4. ☐ Trabalho de migração completa em todos os documentos: `cross-sell-taxonomy.md`, `cross-sell-matrix.csv`, `growth-email.html`, `email-command-center.html`, este template, `taxonomy-quick-reference.md`, `taxonomy-takeaway.md`.
5. ☐ Atualizar memória persistente do Claude (`MEMORY.md` + `project_absolut_taxonomy.md`).

---

## Princípios não-negociáveis

1. **Fato do evento mora 1 vez.** Data, hotel, capacidade ficam só em `00-briefing/`. Nunca duplicar.
2. **Lead mora 1 vez.** Lista única com coluna "publico" classificando. Nunca dividir lista em 4.
3. **Copy é o único que se divide por público.** Em `02-copy/{publico}/`.
4. **Cross-sell mora no silo de ORIGEM.** Porque o tom parte de "você que viveu X".
5. **Frontmatter obrigatório em todo email.** Sem ele, sistema não dispara automação.
6. **Nunca tratar evento como sub-silo.** Super Bowl é evento. NFL é sub-silo. American Sports é silo. Confundir isso quebra a hierarquia.
