# Taxonomia ABSOLUT — Quick Reference

> Cartão de bolso para Jack, Rachella, Victor, Wictor. Imprime e cola na mesa.
> Versão 1.0 · 2026-05-14

---

## Os 3 níveis (decora isso)

```
SILO          →   SUB-SILO       →   EVENTO
─────────         ──────────         ─────────
Categoria         Modalidade         Edição específica
(7 fixas)         (estável)          (muda todo ano)

Ex: american-sports / nfl / super-bowl-lxi
    automobilismo  / f1  / sp-2026
    tenis          / grand-slams / wimbledon-2026
```

---

## Os 7 silos + 2 programas

| Cód | Silo | Sub-silos principais |
| --- | --- | --- |
| 01 | American Sports | NFL · NBA · Golf |
| 02 | Futebol | Libertadores · Sudamericana · Recopa · Flamengo · Copa do Mundo · Brasileiro · Europeu |
| 03 | Automobilismo | F1 SP · F1 Global (22 GPs) · MotoGP Goiânia · MotoGP Global |
| 04 | Esportes Olímpicos | Atletismo · Canoagem · Ginástica · Vôlei · Handball (Fase 2) |
| 05 | Tênis | Grand Slams (AO·RG·Wimbledon·USO) · NFTO |
| 06 | Promocionais ASB | Brand · Storytelling · Bastidores · Posicionamento |
| 07 | Oportunidades de calendário | Datas-gatilho · Newsjacking · Black Friday |
| P01 | ABSOLUT Pass | Assinatura recorrente |
| P02 | Cross-sell | Comprou A → oferta B |

---

## Antes de escrever qualquer email, responda 8 perguntas

| # | Pergunta | Resposta |
| --- | --- | --- |
| 1 | **Público?** | B2C · B2B · B2B2C · HNWI |
| 2 | **Awareness Schwartz?** | Unaware · Problem-Aware · Solution-Aware · Product-Aware · Most-Aware |
| 3 | **Sofisticação do mercado?** | 1 (categoria nova) → 5 (saturado, exige identidade) |
| 4 | **Silo?** | uma das 7 cats / 2 progs |
| 5 | **Sub-silo?** | a modalidade |
| 6 | **Evento?** | a edição |
| 7 | **Tier?** | 1 (template aprovado) · 2 (briefing) · 3 (Mauricio) |
| 8 | **Farol?** | Verde (segue) · Amarelo (aprovação) · Vermelho (nunca) |

**Perguntas 1–3 = estratégia (Schwartz).**
**Perguntas 4–6 = escopo do produto.**
**Perguntas 7–8 = execução e governança.**

---

## Regra de pastas no Drive

```
{silo}/{sub-silo}/{evento}/
   00-briefing/        ← dado do evento (1 lugar só)
   01-leads/           ← base segmentada (1 lugar só)
   02-copy/            ← AQUI divide por público
      b2c/
      b2b/
      b2b2c/
      hnwi/
   03-assets/          ← fotos, vídeos, logos (1 lugar só)
   04-execucao/        ← histórico de envios
   05-cross-sell/      ← emails de saída pra outros silos
```

**Regra de ouro:** se a informação é a mesma pros 4 públicos, fica fora de `02-copy/`. **Nunca duplicar evento inteiro por público.**

---

## Matriz cross-sell (modalidade → modalidade)

| Comprou ↓ | Oferta `A` (forte) | Oferta `M` (média) | Oferta `B` (não) |
| --- | --- | --- | --- |
| NFL (inclui SB) | NBA · Golf · F1 · Grand Slams · Copa do Mundo | NFL Int. Series · MotoGP · NFTO | Sudamericana · Recopa · Flamengo |
| F1 (SP + Global) | NFL · NBA · Golf · MotoGP · Grand Slams · NFTO · Copa do Mundo | Libertadores · Flamengo | Sudamericana · Recopa · Olímpicos |
| Grand Slams | NFL · NBA · Golf · F1 · NFTO · Copa do Mundo | Libertadores · Flamengo · MotoGP · Olímpicos | Sudamericana · Recopa |
| Golf | F1 · Grand Slams · NFTO | NFL · NBA · Copa do Mundo | Futebol (tudo) · MotoGP · Olímpicos |
| Libertadores | Sudamericana · Recopa · Flamengo · Copa do Mundo | NFL · NBA · F1 · Grand Slams · NFTO | Golf · MotoGP · Olímpicos |
| Flamengo | Libertadores · Copa do Mundo | Sudamericana · Recopa · NBA · F1 · Grand Slams · NFTO | NFL · Golf · MotoGP · Olímpicos |
| Copa do Mundo | (cross-sell para quase tudo — público mais largo) | Olímpicos · MotoGP | — |
| NFTO | Golf · F1 · Grand Slams | NFL · NBA · Futebol BR · MotoGP · Olímpicos · Copa do Mundo | — |
| MotoGP | F1 | Copa do Mundo · Grand Slams · NFTO · Olímpicos | NFL · NBA · Golf · Futebol |
| Olímpicos | — | Copa do Mundo · Grand Slams · NFTO | tudo o resto |

**Regra:** afinidade `A` = disparar email em 30 dias · `M` = newsletter segmentada 60–120 dias · `B` = não ofertar ativamente.

Matriz completa (169 pares): `cross-sell-matrix.csv`.

---

## Frontmatter padrão de todo email

Cola no topo de todo arquivo de copy. **Obrigatório.**

```yaml
---
silo-origem: american-sports/nfl
evento-origem: super-bowl-lxi
silo-destino:                  # vazio se venda direta; preenche se cross-sell
evento-destino:
tipo: aquisicao                # aquisicao | nurturing | venda-direta | cross-sell | win-back | onboarding
publico-alvo: HNWI             # B2C | B2B | B2B2C | HNWI
schwartz-awareness: most-aware
schwartz-sophistication: 5
hook-principal: identidade     # promessa | mecanismo | identidade | preco
tier: 3
farol: amarelo
autor: Mauricio
data-criacao: 2026-05-14
---
```

---

## Erros comuns a evitar

- ❌ Tratar Super Bowl como silo de topo (é evento dentro de NFL)
- ❌ Duplicar pasta de evento por público (B2C/, B2B/ no nível do evento)
- ❌ Ofertar afinidade `B` para cliente que comprou silo X (gasta credibilidade)
- ❌ Escrever email Tier 3 sem passar pelo Mauricio
- ❌ Pular o frontmatter (sem ele, sistema não sabe disparar cross-sell)
- ❌ Ignorar Schwartz: tratar cliente Most-Aware como se fosse Unaware (chato e ofensivo) ou vice-versa (vende menos)

---

## Quando precisar consultar

| Pergunta | Onde |
| --- | --- |
| Como classifico um novo evento? | `cross-sell-taxonomy.md` §2 |
| Qual o score de afinidade entre X e Y? | `cross-sell-matrix.csv` |
| Qual hook usar (promessa/mecanismo/identidade)? | Schwartz §1.1 + Camada Zero (a integrar) |
| Quando disparar o cross-sell? | `cross-sell-taxonomy.md` §4 (regras de gatilho RD) |
| Estrutura de pastas exata? | `taxonomy-folder-template.md` |
