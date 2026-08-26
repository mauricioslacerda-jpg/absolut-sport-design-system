# Cross-Sell Taxonomy — ABSOLUT Sport

> Modelo de taxonomia para permitir cross-sell sistemático entre silos, sub-silos e públicos. Vive ao lado do `growth-email.html` e alimenta automações no RD Station.

**Versão:** 1.0 · 2026-05-14
**Autor:** Mauricio Lacerda
**Status:** Beta — aplicar em piloto (Super Bowl LXI → F1 SP) antes de propagar

---

## 1. Princípio

Cross-sell não é "quem comprou A pode gostar de B". Cross-sell é **mover um cliente entre eventos de sub-silos diferentes respeitando 3 eixos simultâneos**:

1. **Afinidade de produto** — Super Bowl (NFL) e F1 SP compartilham público AB+ premium; Flamengo e NFTO não.
2. **Janela de calendário** — vender F1 SP em outubro pra quem comprou SB em fevereiro funciona; vender em março não (longe demais).
3. **Estágio Schwartz do cliente** — quem já comprou SB é **Most Aware** do produto ABSOLUT (não do próximo evento). Copy de cross-sell parte de identidade ("você que viveu o SB"), não de promessa básica.

A taxonomia abaixo codifica os 3 eixos como **metadados estruturados** em cada lead, evento e email — para que o RD Station consiga disparar automações sem intervenção humana.

### 1.1 Glossário de hierarquia (3 níveis)

| Nível | Exemplo | O que é |
| --- | --- | --- |
| **Silo** | `american-sports` · `automobilismo` · `tenis` | Categoria macro. 7 hoje. Fixo. |
| **Sub-silo** | `nfl` · `nba` · `golf` · `f1` · `motogp` · `grand-slams` · `nfto` | Modalidade esportiva. Estável ao longo dos anos. Onde a matriz de afinidade opera. |
| **Evento** | `super-bowl-lxi` · `f1-sp-2026` · `wimbledon-2026` | Instância temporal. Muda todo ano. Onde leads são atribuídos, copy é escrito, vendas acontecem. |

Regra: **matriz e automação operam em sub-silo. Copy e leads operam em evento.**

---

## 2. Três camadas da taxonomia

### Camada A — Atributos do **Silo/Sub-silo** (fixo, por evento)

Cada sub-silo recebe um conjunto de tags estruturais. Exemplo:

```yaml
silo: american-sports
sub-silo: nfl
evento: super-bowl-lxi
data: 2026-02-08
janela-venda: 2025-09 a 2026-02
ticket-base: USD 6000
ticket-teto: USD 18000
publico-dominante: [B2C, HNWI]
publico-secundario: [B2B, B2B2C]
sofisticacao-schwartz: 5
geografia: internacional-eua
modalidade: presencial-deslocamento
duracao: 4 dias
afinidades:
  alta: [f1-sp, grand-slams-us-open, nba-finals]
  media: [nfl-int-series, libertadores-final, masters-augusta]
  baixa: [futebol-brasileiro, motogp-goiania]
```

Os campos `afinidades` é o coração do cross-sell. Eles não são chutados — derivam de 3 critérios:

| Critério | Peso |
|---|---|
| **Compartilhamento de público dominante** | 40% |
| **Compatibilidade de ticket** (mesma ordem de grandeza ±50%) | 30% |
| **Distância de calendário** (60–180 dias entre eventos) | 30% |

### Camada B — Atributos do **Lead** (dinâmico, atualizado a cada compra)

Cada lead na base do RD Station carrega:

```yaml
lead-id: 12345
nome: Daniel Pereira
publico: HNWI            # B2C | B2B | B2B2C | HNWI
eventos-comprados: [super-bowl-lxi-2024, f1-sp-2025]
eventos-consultados: [wimbledon-2026]              # abriu email, clicou, não comprou
silos-ativos: [american-sports/nfl, automobilismo/f1]
ticket-historico-medio: USD 14500
ticket-historico-max: USD 22000
ultimo-evento: 2025-11-09
proximo-elegivel-window: 2026-01-15 a 2026-06-30
schwartz-stage: most-aware-asb     # most-aware-asb | product-aware | solution-aware | problem-aware | unaware
preferencia-geografia: [internacional, brasil-sp]
preferencia-modalidade: [presencial-deslocamento]
flags: [vip-curado, hnwi-verificado, paga-em-usd]
```

A coluna `schwartz-stage` é decisiva: cliente que já comprou ABSOLUT está **Most Aware da marca** mesmo sendo Problem-Aware do próximo silo. Isso muda o tom do email — é cross-sell, não aquisição.

### Camada C — Atributos do **Email** (cada peça de copy)

Todo email gerado declara, no frontmatter:

```yaml
silo-origem: american-sports/nfl
evento-origem: super-bowl-lxi
silo-destino: automobilismo/f1
evento-destino: f1-sp-2026   # vazio se for venda direta do silo de origem
tipo: cross-sell             # aquisicao | nurturing | venda-direta | cross-sell | win-back | onboarding
publico-alvo: HNWI
schwartz-awareness: most-aware
schwartz-sophistication: 4
hook-principal: identidade   # promessa | mecanismo | identidade | preco
tier: 3
farol: amarelo
```

---

## 3. Matriz de afinidade — nível **sub-silo (modalidade)**

A matriz opera em nível de **sub-silo (modalidade esportiva)**, não evento. Razão: eventos são instâncias temporais ("Super Bowl LXI 2026") que mudam todo ano; sub-silos ("NFL", "F1", "Grand Slams") são estáveis. Manter a matriz em nível de modalidade evita reescrita anual.

Lê-se: **se cliente comprou evento do sub-silo {linha}, oferecer eventos do sub-silo {coluna} com prioridade {valor}**.

| ↓ Comprou \ Ofertar → | NFL | NBA | Golf | Libertadores | Sudamericana | Recopa | Flamengo | Copa do Mundo | F1 | MotoGP | Olímpicos | Grand Slams | NFTO |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **NFL** (inclui SB) | — | **A** | A | M | B | B | B | A | **A** | M | B | **A** | M |
| **NBA** | A | — | M | M | B | B | B | A | A | B | B | A | M |
| **Golf** (Masters/PGA) | M | M | — | B | B | B | B | M | **A** | B | B | **A** | A |
| **Libertadores** | M | M | B | — | **A** | **A** | **A** | **A** | M | B | B | M | M |
| **Sudamericana** | B | B | B | **A** | — | **A** | M | A | B | B | B | B | M |
| **Recopa** | B | B | B | **A** | **A** | — | M | A | B | B | B | B | M |
| **Flamengo** | B | M | B | **A** | M | M | — | **A** | M | B | B | M | M |
| **Copa do Mundo** | A | A | M | A | A | A | A | — | A | M | M | A | M |
| **F1** (SP + Global) | **A** | A | A | M | B | B | M | A | — | **A** | B | **A** | A |
| **MotoGP** | B | B | B | B | B | B | B | M | **A** | — | B | M | M |
| **Olímpicos** | B | B | B | B | B | B | B | M | B | B | — | M | M |
| **Grand Slams** | **A** | A | **A** | M | B | B | M | A | **A** | M | M | — | **A** |
| **NFTO** | M | M | A | M | M | M | M | M | A | M | M | **A** | — |

**Legenda:** `A` = afinidade alta (disparar email em até 30 dias) · `M` = média (incluir em newsletter segmentada, 60–120 dias) · `B` = baixa (não ofertar ativamente; só se cliente sinalizar interesse).

**Negrito** = afinidade especialmente forte, candidato a campanha dedicada.

### 3.1 Refinamento por evento (override pontual)

Eventos específicos podem ter afinidade diferente da modalidade-pai. Ex: **Super Bowl** tem afinidade `A` com **F1 SP** (B2B HNWI sobrepõe), mas **NFL Regular Season** tem afinidade `M`. Esses overrides vivem em `silos.csv` como linha extra:

```csv
origem,destino,score,nota
nfl/super-bowl,f1/sp,A,publico hnwi sobreposto
nfl/regular-season,f1/sp,M,publico b2c sobreposto apenas parcial
golf/masters,grand-slams/wimbledon,A,prestigio + abril/julho proximos
```

Quando existe override por evento, o RD Station usa o override; caso contrário, cai pra matriz da modalidade.

---

## 4. Regras de gatilho para automação no RD Station

Cada regra é uma automação. Nome no formato `XSELL_{origem}__{destino}__{publico}`.

| Gatilho | Condição | Ação |
| --- | --- | --- |
| **Compra concluída em evento X** | `eventos-comprados` recebe novo valor | Esperar 14 dias → consultar matriz no sub-silo de X → enviar email cross-sell para próximo evento do sub-silo de afinidade `A` mais próxima no calendário, no público dominante do lead |
| **Janela ideal de cross-sell** | `proximo-elegivel-window` começa hoje E `eventos-consultados` contém evento Y cujo sub-silo tem afinidade `A` ou `M` com sub-silo já comprado | Disparar sequência de 3 emails do evento Y para o público do lead |
| **Abandono de consulta** | Lead abriu 3+ emails do evento Y em 30 dias E não comprou | Reclassificar `schwartz-stage` para `product-aware` e mover para sequência de nurturing do sub-silo de Y |
| **Aniversário de compra** | 11 meses após `ultimo-evento` | Disparar win-back do mesmo evento (próxima edição) OU cross-sell de evento em sub-silo de afinidade `A`, escolhendo o que tiver janela de venda aberta |
| **Calendário-gatilho oportunístico** | Evento Z (Cat. 07) aconteceu (final inesperada, lesão, etc.) | Disparar email do silo Z para todos os leads com afinidade `A` ou `M` no sub-silo correspondente, no público dominante |

---

## 5. Estrutura de pastas no Drive (reflete a taxonomia)

```
/ABSOLUT-Sport-Operacao/
   /00-Taxonomia/
      cross-sell-matrix.csv          ← matriz de afinidade exportada
      schwartz-decision-tree.md       ← qual hook usar em cada quadrante
      publicos-definicao.md           ← B2C, B2B, B2B2C, HNWI
   /01-American-Sports/                ← SILO
      /NFL/                            ← sub-silo (modalidade)
         /Super-Bowl-LXI/              ← evento específico
            00-briefing/               ← dado do evento (1 lugar)
            01-leads/                  ← base segmentada (1 lugar)
            02-copy/
               /b2c/
               /b2b/
               /b2b2c/
               /hnwi/
            03-assets/
            04-execucao/
            05-cross-sell/             ← emails de saída para outros silos
               para-f1-sp/
               para-grand-slams/
               para-nfl-int-series/
         /NFL-International-Series/    ← outro evento dentro do mesmo sub-silo NFL
      /NBA/                            ← sub-silo (modalidade)
         /NBA-Regular-Season/
         /NBA-Finals/
      /Golf/                           ← sub-silo (modalidade)
         /Masters-Augusta/
         /PGA-Championship/
         /US-Open-Golf/
         /The-Open-Championship/
   /02-Futebol/
      /Libertadores/
      /Sudamericana/
      /Recopa/
      /Flamengo/
      /Copa-do-Mundo/
   /03-Automobilismo/
      /F1-SP-Interlagos/
      /F1-Global/
         /Australia/  /China/  /Japao/  /Miami/  /Canada/  /Monaco/
         /Espanha/    /Austria/ /UK/    /Belgica/ /Hungria/ /Holanda/
         /Italia/     /Madrid/ /Baku/  /Singapura/ /Austin/ /Mexico/
         /Las-Vegas/  /Catar/  /Abu-Dhabi/
      /MotoGP-Goiania/
      /MotoGP-Global/
   /04-Olimpicos/
      /Atletismo/  /Canoagem/  /Ginastica/  /Volei/  /Handball/
   /05-Tenis/
      /Grand-Slams/
         /Australian-Open/  /Roland-Garros/  /Wimbledon/  /US-Open/
      /NFTO-Brasil/
   /06-Promocionais-ASB/
   /07-Oportunidades-Calendario/
   /Prog-01-ABSOLUT-Pass/
   /Prog-02-Cross-Sell/                ← apenas governança; copy real vive em /05-cross-sell/ de cada silo de origem
      campanhas-multi-silo/
      sequencias-aniversario/
      win-back/
```

**Princípio da pasta `05-cross-sell/`:** copy de cross-sell mora no **silo de origem** (de onde o cliente está saindo), não no de destino. Porque o tom de voz parte de "você que viveu X" e isso é responsabilidade da equipe que conhece X.

---

## 6. Como o RD Station consome a taxonomia

Três tabelas mestre que vivem como Custom Fields no RD Station ou em Google Sheets sincronizada:

1. **`silos.csv`** — atributos da Camada A (1 linha por sub-silo, ~30 linhas)
2. **`afinidade-matrix.csv`** — matriz da seção 3 em formato long (origem, destino, score)
3. **`schwartz-rules.csv`** — qual hook usar em cada combinação `(awareness × sophistication × publico)`

O Victor configura as automações no RD lendo essas três tabelas. Quando você adicionar um silo novo (digamos, Champions League), basta:
1. Adicionar linha em `silos.csv`
2. Adicionar coluna+linha em `afinidade-matrix.csv` com os scores
3. Nenhuma automação nova precisa ser criada — elas leem a matriz dinamicamente

---

## 7. Piloto e validação

**Piloto:** evento `american-sports/nfl/super-bowl-lxi` (fevereiro 2026) → evento `automobilismo/f1/sp` (novembro 2026). 9 meses entre eventos. Afinidade de modalidade NFL→F1 = `A`. Override por evento mantém `A`. Público dominante: HNWI + B2B.

**Sequência piloto:**
- D+14 pós-SB: email de agradecimento + teaser F1 SP ("o próximo capítulo")
- D+45: case real de cliente que veio do SB e foi pro F1
- D+90: abertura formal de vendas F1 SP com prioridade pra base SB
- D+180: lembrete de janela fechando + upgrade pra camarote

**Métrica de sucesso:** % da base SB que compra F1 SP no mesmo ciclo. Baseline atual (sem cross-sell estruturado): ~chutado. Meta piloto: 15% conversão na base HNWI, 8% na base B2B.

**Próximo par a aplicar após piloto:** `tenis/grand-slams/wimbledon` → `automobilismo/f1/silverstone-uk` (mesma geografia, mesma janela de julho, público HNWI internacional, afinidade modalidade `A`).

---

## 8. O que esta taxonomia NÃO resolve

- **Aquisição fria** (lead que nunca comprou) — isso é jornada de aquisição, não cross-sell.
- **Win-back de >24 meses** — lead frio precisa de re-aquisição, não cross-sell.
- **B2B2C cross-sell para o consumidor final** — operadora de cartão vendendo experiência pro portador é problema da operadora, não da ABSOLUT.
- **Cross-sell entre tier de ticket muito diferente** (ex: NFTO R$3k → Grand Slam R$30k) — exige sequência de nurturing dedicada antes do cross-sell direto.

---

## 9. Próximos passos

1. Exportar `cross-sell-matrix.csv` da seção 3 (1 dia)
2. Criar `silos.csv` com atributos da Camada A para os 7 silos atuais (2 dias com Wictor revisando)
3. Adicionar campos Camada B no RD Station (Victor — 1 semana)
4. Reescrever 4 emails do piloto SB → F1 SP usando frontmatter Camada C (Mauricio — 3 dias)
5. Ligar automação no RD (Victor — 1 semana)
6. Rodar piloto durante 2026-02 a 2026-11
7. Auditar resultado em dezembro de 2026 e propagar para os outros silos
