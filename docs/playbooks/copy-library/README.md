# Copy Library — Biblioteca de Respostas da Aby

Biblioteca canônica de respostas rápidas da Aby (bot ABSOLUT Sport), com sistema de variáveis para reuso por evento.

- **Fonte:** [Google Sheets](https://docs.google.com/spreadsheets/d/1UAjsxfeR_23Cl-wNtztzw4QkP1RxoBkk4rrDFFojiyc/edit#gid=1469143387) (gid 1469143387)
- **Página viva:** [`../copy-library.html`](../copy-library.html)
- **Versão atual:** v2-2026-06-02 · 35 mensagens · 13 categorias · 13 variáveis

## Arquivos desta pasta

| Arquivo | Função |
| --- | --- |
| `extract.py` | Script Python que lê `input.tsv` e gera todos os JSONs abaixo |
| `input.tsv` | Export da planilha em formato markdown/tsv (fonte do parser) |
| `messages.json` | Dados estruturados das 35 mensagens (ID, categoria, atalho, vars, chaves i18n) |
| `variables.json` | Dicionário das 13 variáveis (com chaves i18n) |
| `i18n-keys.json` | Mapa completo de chaves `data-i18n` usadas pela página |
| `i18n-pt.json` | Dicionário PT (fonte da verdade) |
| `i18n-en.json` · `i18n-es.json` · `i18n-de.json` | Stubs com UI traduzida e conteúdo de mensagens marcado como `[TODO LANG]` |

## Como atualizar quando a planilha mudar

```bash
cd "G:/Meu Drive/ABSOLUT Sport Design System/playbooks/copy-library"
python extract.py --online       # baixa direto da planilha (precisa de `requests`)
# OU
# 1. Abra a planilha no Google Sheets
# 2. Exporte como markdown ou cole na MCP Drive
# 3. Substitua `input.tsv`
python extract.py                # gera tudo a partir do input.tsv
python extract.py --validate     # só valida sem regenerar
```

Após qualquer regeneração, commit dos JSONs para o git — a página HTML consome os arquivos via `fetch()`.

## Como traduzir para EN/ES/DE

1. Abra `i18n-en.json` (ou ES/DE)
2. Substitua linhas com prefixo `[TODO EN]` pela tradução real
3. Mantenha as variáveis `{nome}`, `{url}`, etc. **intactas** — são placeholders
4. Salve. A página atualiza automaticamente.

A UI (botões, labels) já vem traduzida no stub — só conteúdo de mensagens, observações e exemplos de variáveis estão pendentes.

## Princípios não-negociáveis

1. **A20 (Política de cancelamento) é texto contratual.** Não alterar sem revisão jurídica.
2. **Variáveis são genéricas.** Para usar com outro evento, mude apenas o dicionário (`i18n-pt.json` campos `lib.var.*.example`), nunca a copy.
3. **Append-only no histórico de versões.** Versão atual: v2-2026-06-02. Próxima edição = v3, manter changelog no rodapé.

## Relação com a Aby

Quatro mensagens (`A24`, `A25`, `A26`, `A28`) mapeiam para itens da auditoria do bot Aby:

| ID | Item da auditoria |
| --- | --- |
| A24 — falar com humano | 01/03 (handoff humano) |
| A25 — floodado | 31 (uso do tempo de fila) |
| A26 — ganhar tempo | 04 (fallback gracioso) |
| A28 — ghosting | 32 (encerramento explícito) |

Esta biblioteca é a **fonte canônica** para automatizar esses fluxos no bot.
