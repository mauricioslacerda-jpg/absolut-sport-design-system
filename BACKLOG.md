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
