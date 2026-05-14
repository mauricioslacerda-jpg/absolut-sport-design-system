# ABSOLUT Sport Design System — Backlog

Ideias e iniciativas pendentes. Cada item: responsável, autor da ideia, status, contexto.

---

## Substituir selo MIT no Enterprise AI Playbook

- **ID:** BL-004
- **Autor:** Mauricio Lacerda
- **Registrado em:** 2026-05-11
- **Status:** Pendente — execução manual por Mauricio

### Resumo
Substituir o asset do selo MIT em `playbooks/enterprise-ai.html:888` (atualmente `../assets/mit-seal.svg`) por um novo logo MIT a ser curado por Mauricio.

### Contexto
Em 11/05/2026 surgiu um PNG (`assets/download.png`, 4.9KB, logo MIT raster) candidato à substituição. Foi descartado pra Mauricio fazer a curadoria do asset definitivo (formato, qualidade, fonte oficial). O PNG foi deletado no toalette do dia.

---

## Acesso restrito + versões pocket por audiência

- **ID:** BL-001
- **Autor da ideia:** Felipe Machado (felipe.machado@absolut-sport.com.br)
- **Registrado por:** Mauricio Lacerda — 2026-04-30
- **Status:** Backlog (não iniciado)
- **Asana:** task criada no projeto do Felipe — vincular GID quando arrancar

### Resumo
Criar camada de autenticação no Design System (login/senha) com **distinção de níveis de acesso por domínio** e gerar **versões pocket** do sistema, uma por propósito de audiência.

### Distinção por domínio
- `@absolut-sport.com.br` → acesso interno completo (e variantes do domínio principal)
- Domínios externos → acesso restrito por papel

### Versões pocket — uma por audiência
- **Influencers** — kit reduzido: logos, cores, tom, do/don't de uso de marca, hashtags oficiais
- **Parceiros** — co-branding rules, logos co-marcados, templates de ativação
- **Mídia / Imprensa** — press kit, fact sheet da empresa, bios, fotos em alta
- (outras audiências a definir conforme demanda)

### Por que é uma boa ideia
- Hoje o Hub é público (qualquer URL acessa) — bom para distribuição livre dos 4 escritórios, ruim quando há conteúdo sensível ou contratual (parceiros, briefings de mídia).
- Versões pocket evitam jogar o Hub inteiro em audiências que só precisam de 5% dele. Reduz fricção e protege guidelines internas.

### Pontos a resolver antes de implementar
- Auth provider: Cloudflare Access (já estamos no Pages) vs. solução própria
- Como manter a paridade de tokens entre Hub principal e pockets sem duplicação (single source: `colors_and_type.css`)
- Fluxo de convite/revogação de acesso para parceiros e mídia
- Métricas: o que medir em cada pocket (acessos, downloads de brand kit, etc.)

### Próximos passos (quando arrancar)
1. Validar com Felipe quais audiências entram no MVP
2. Decidir auth provider
3. Prototipar uma pocket (sugestão: Mídia, é a mais autocontida)
4. Definir governança de acesso

---

## ABSOLUT Players — cards de staff no Hub

- **ID:** BL-002
- **Autor da ideia:** Mauricio Lacerda
- **Registrado por:** Mauricio Lacerda — 2026-04-30
- **Status:** Backlog (não iniciado)

### Resumo
Página/seção no Hub do Design System com **cards de cada "ABSOLUT Player"** (staff). Cada card carrega:
- Nome, foto, cargo, escritório (Rio / Frankfurt / LA / Buenos Aires)
- **Responsabilidades** (áreas/projetos sob ownership)
- **Contatos** (email, WhatsApp, Slack/handles internos)
- **Atualização de projetos** ativos com status (em andamento, bloqueado, entregue)

### Por que
- Hoje não há referência única de "quem faz o quê" na ABSOLUT distribuída em 4 escritórios.
- O Hub do DS já é o ponto de gravidade público da empresa — colocar Players ali transforma o DS em diretório vivo, não só catálogo de marca.
- Funciona como handshake para parceiros e mídia (paridade com a ideia BL-001).

### Pontos a resolver
- Fonte de verdade dos dados (Asana? Google Workspace directory? planilha?)
- Visibilidade: público no Hub vs. atrás do auth (depende de BL-001)
- Como manter status de projetos sincronizado sem virar trabalho manual
- Layout dos cards (vertical com foto full-bleed seguindo a estética do DS)

### Próximos passos (quando arrancar)
1. Decidir fonte de dados
2. Definir schema do "Player" (campos obrigatórios vs opcionais)
3. Prototipar 1 card e validar com 2-3 Players
4. Decidir gating (público vs autenticado — alinhar com BL-001)

---

## Input de sugestões + navbar lateral no Hub

- **ID:** BL-003
- **Autor da ideia:** Mauricio Lacerda
- **Registrado por:** Mauricio Lacerda — 2026-04-30
- **Status:** Backlog (não iniciado)

### Resumo
Duas melhorias de UX no Hub:
1. **Input de sugestões** — campo persistente "envie uma sugestão / reporte um problema" em todas as páginas do Hub. Hoje a única via é `design@absolut-sport.com.br`, que tem fricção alta (abrir cliente de email, escrever do zero).
2. **Navbar lateral** — navegação persistente na lateral esquerda, listando seções do Hub (Foundations, Components, Playbooks, Players, etc.). Hoje a navegação é só pelo `index.html` como ponto de entrada.

### Por que
- Hub está crescendo (Foundations, Playbooks, em breve Players + Pockets) — sem nav lateral o usuário se perde ou não descobre o que existe.
- Input de sugestões fecha o loop de feedback diretamente onde a pessoa está usando o sistema, sem trocar de contexto.

### Pontos a resolver
- Onde as sugestões aterrissam: form → email para `design@`? Asana? Issue tracker?
- Navbar precisa funcionar tanto no Hub quanto nos playbooks-filhos (consistência de markup)
- Mobile: navbar vira drawer? hidden por trás de hamburger?
- Estado ativo da navbar quando o conteúdo é embed iframe no Shopify

### Próximos passos (quando arrancar)
1. Decidir destino das sugestões (recomendo: form → Asana via webhook)
2. Definir estrutura de navegação (lista canônica de seções)
3. Prototipar navbar em uma página, ajustar tokens de espaçamento
4. Replicar pattern em todas as páginas-filhas

---

## Migrar Email Command Center para taxonomia 7 silos + 2 programas (3 níveis)

- **ID:** BL-005
- **Autor:** Mauricio Lacerda
- **Registrado em:** 2026-05-14
- **Status:** Pendente — aguardando piloto cross-sell SB→F1 SP estabilizar

### Resumo
O `email-command-center.html` foi construído sob a taxonomia legada de **6 silos** (Super Bowl LXI · Futebol · F1 · Tênis · ABSOLUT Pass · Cross-sell). A nova taxonomia canônica é **7 silos + 2 programas em 3 níveis** (silo → sub-silo → evento), definida em `playbooks/cross-sell-taxonomy.md` e já refletida em `playbooks/growth-email.html`.

### Escopo da migração
1. **Renomear/criar abas** — substituir as 6 abas atuais por:
   - American Sports (NFL · NBA · Golf)
   - Futebol (Libertadores · Sudamericana · Recopa · Flamengo · Copa do Mundo · Brasileiro · Europeu)
   - Automobilismo (F1 SP · F1 Global · MotoGP Goiânia · MotoGP Global)
   - Esportes Olímpicos (Atletismo · Canoagem · Ginástica · Vôlei · Handball — Fase 2)
   - Tênis (Grand Slams · NFTO)
   - Promocionais ASB
   - Oportunidades de calendário
   - ABSOLUT Pass (programa)
   - Cross-sell (programa)
2. **Adicionar drill-down sub-silo → evento** dentro de cada aba de silo (hoje só tem 1 nível).
3. **Integrar matriz de afinidade** da `cross-sell-taxonomy.md` como aba ou widget visual.
4. **Sincronizar i18n** PT/EN/ES/DE (4 idiomas, paridade com `growth-email.html`).
5. **Atualizar stat "6 silos" → "7 silos + 2 programas"** em todos os pontos da UI (já feito nos pontos mais visíveis em 2026-05-14, mas os 6 cards `silo-card` legados continuam em produção).

### Por que não foi feito ainda
- A reestruturação é UI-pesada (cerca de 500 linhas de HTML/CSS afetadas) e exige decisão visual sobre drill-down (acordeão, sub-abas, modal).
- Faz mais sentido esperar o piloto cross-sell SB→F1 SP rodar (fev–nov 2026) e validar a matriz antes de cristalizar a UI.
- Em 2026-05-14 foi feita atualização superficial: meta tags, intro, stat numérico — mas as 6 abas e 6 cards continuam estruturalmente legados.

### Pontos a resolver antes de implementar
- Visualização do drill-down sub-silo → evento (acordeão? tabs aninhadas? modal?)
- Como mostrar a matriz de afinidade 13×13 sub-silos numa UI legível em mobile
- Sincronização com `silos.csv` / `cross-sell-matrix.csv` (planejados na taxonomia §6) — deve ler dinamicamente ou ser estático?
- Migração das URLs/anchors existentes (`#silo-sblxi`, `#silo-futebol`…) sem quebrar bookmarks externos

### Próximos passos (quando arrancar)
1. Prototipar drill-down sub-silo em uma aba (sugestão: começar por Automobilismo, que tem mais sub-silos e expõe o problema)
2. Definir esquema visual da matriz de afinidade
3. Reescrever as 9 seções (7 silos + 2 programas) seguindo o template novo
4. Atualizar tabs + i18n + analytics events
5. Manter redirecionamento dos anchors antigos por 1 ciclo (até 2026-12)
