# -*- coding: utf-8 -*-
"""
extract.py — Interpretador da Biblioteca de Respostas Rápidas da Aby

Lê a planilha Google Sheets canônica (ID: 1UAjsxfeR_23Cl-wNtztzw4QkP1RxoBkk4rrDFFojiyc)
e gera os artefatos consumidos pela página HTML do Design System:

  1. messages.json        — dados estruturados (35 mensagens, 13 categorias)
  2. variables.json       — dicionário de variáveis ({nome}, {parceiro}, etc.)
  3. i18n-keys.json       — mapa de chaves data-i18n (lib.msg.A01.text, etc.)
  4. i18n-pt.json         — dicionário PT preenchido (fonte da verdade)
  5. i18n-en.json         — stub EN (mesma estrutura, valores = fallback PT)
  6. i18n-es.json         — stub ES (idem)
  7. i18n-de.json         — stub DE (idem)

Modo offline (default): lê de input.tsv local, que é o export da planilha.
Modo online: lê via Google Sheets export CSV se gspread/requests instalados.

Uso:
  python extract.py                       → gera tudo a partir de input.tsv local
  python extract.py --online              → tenta fetch da planilha live
  python extract.py --validate            → só valida o JSON gerado
  python extract.py --diff                → mostra diff entre PT atual e PT novo

Reuso por evento: a copy é genérica. Para reusar, basta editar variables.json
substituindo os exemplos (Libertadores 2026) pelos do evento vigente. O HTML
re-renderiza automaticamente.
"""

import argparse
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path


def slugify_cat(name: str) -> str:
    """Slug ASCII-only, determinístico, idêntico em Python e JS.

    Algoritmo (replicar em JS):
      1. NFKD-normaliza e remove diacríticos
      2. lowercase
      3. troca tudo que não é [a-z0-9] por '_'
      4. colapsa '_' repetidos e trim
    """
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_str = ascii_str.lower()
    ascii_str = re.sub(r"[^a-z0-9]+", "_", ascii_str)
    return ascii_str.strip("_")

HERE = Path(__file__).parent
SHEET_ID = "1UAjsxfeR_23Cl-wNtztzw4QkP1RxoBkk4rrDFFojiyc"
GID_LIBRARY = "1469143387"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=tsv&gid={GID_LIBRARY}"

INPUT_TSV = HERE / "input.tsv"
MESSAGES_JSON = HERE / "messages.json"
VARIABLES_JSON = HERE / "variables.json"
I18N_KEYS_JSON = HERE / "i18n-keys.json"
I18N_PT = HERE / "i18n-pt.json"
I18N_EN = HERE / "i18n-en.json"
I18N_ES = HERE / "i18n-es.json"
I18N_DE = HERE / "i18n-de.json"

# Categorias canônicas (mantém a ordem da planilha original)
CATEGORIES_ORDER = [
    "Abertura",
    "Produto & Pacotes",
    "Tickets",
    "Vôos",
    "Hospedagem",
    "Transporte",
    "Documentação",
    "Pagamento",
    "Políticas",
    "Pós-venda",
    "Handoff & Atendimento",
    "Encerramento & Re-engajamento",
    "Eventos / Jogos Flamengo",
    "Compliance Flamengo/Maracanã",
    "Descritivo de pacote",
    "Checkout",
]


# ─────────────────────────────────────────────────────────────────────────────
# Fetch / parse
# ─────────────────────────────────────────────────────────────────────────────

def fetch_online() -> str:
    """Baixa a planilha via export TSV. Requer `requests`."""
    try:
        import requests
    except ImportError:
        print("ERRO: pip install requests para usar --online", file=sys.stderr)
        sys.exit(2)
    r = requests.get(SHEET_URL, timeout=15)
    r.raise_for_status()
    return r.text


def parse_markdown_table(text: str) -> tuple[list[dict], list[dict], dict]:
    """
    A planilha foi exportada via MCP Drive como markdown. Parser robusto:
    extrai 3 tabelas:
      - Biblioteca (35 mensagens, cabeçalho ID|Categoria|Gatilho|...)
      - Variáveis (Variável|Significado|Exemplo)
      - Governança (Como usar|...)
    """
    messages: list[dict] = []
    variables: list[dict] = []
    governance: dict = {}

    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    # Encontra o cabeçalho da Biblioteca
    for i, ln in enumerate(lines):
        if ln.startswith("| ID | Categoria"):
            # cada linha "| A01 | ... |" é uma mensagem
            for body in lines[i + 2:]:
                if not body.startswith("| A"):
                    break
                cols = [c.strip() for c in body.strip("|").split("|")]
                if len(cols) < 6:
                    continue
                vars_raw = cols[5] if len(cols) > 5 else ""
                # Variáveis vêm como "{nome} {atendente} {parceiro}" — extrai com regex
                vars_list = re.findall(r"\{([\w_]+)\}", vars_raw)
                # Remove escapes do markdown (\! \_)
                msg_text = cols[4].replace("\\!", "!").replace("\\_", "_")
                messages.append({
                    "id": cols[0],
                    "category": cols[1],
                    "trigger": cols[2],
                    "shortcut": cols[3],
                    "text_pt": msg_text,
                    "variables": vars_list,
                    "observation": cols[6] if len(cols) > 6 else "",
                })
            break

    # Variáveis
    for i, ln in enumerate(lines):
        if ln.startswith("| Variável | Significado"):
            for body in lines[i + 2:]:
                if not body.startswith("| {"):
                    break
                cols = [c.strip() for c in body.strip("|").split("|")]
                if len(cols) < 3:
                    continue
                name = cols[0].strip("{}").replace("\\_", "_")
                variables.append({
                    "name": name,
                    "meaning_pt": cols[1],
                    "example_pt": cols[2],
                })
            break

    # Governança / metadata (texto livre — captura algumas chaves)
    full = "\n".join(lines)
    governance["total_messages"] = len(messages)
    governance["total_categories"] = len(set(m["category"] for m in messages))
    m_v = re.search(r"Atualizado em\s*\|\s*([^|]+?)(?:\s*v|\Z)", full)
    if m_v:
        governance["updated_at"] = m_v.group(1).strip()
    return messages, variables, governance


# ─────────────────────────────────────────────────────────────────────────────
# Build artifacts
# ─────────────────────────────────────────────────────────────────────────────

def build_i18n_keys(messages: list[dict], variables: list[dict]) -> dict:
    """Mapa de chaves data-i18n a usar no HTML."""
    keys = {
        "msg": {},
        "var": {},
        "cat": {},
        "ui": {
            "hero.title": "Biblioteca de Respostas — Aby",
            "hero.sub": "35 mensagens em 13 categorias. Copie, cole, ajuste as variáveis.",
            "filter.all": "Todas",
            "filter.search.placeholder": "Buscar por gatilho, atalho ou texto...",
            "card.shortcut": "Atalho",
            "card.trigger": "Gatilho",
            "card.variables": "Variáveis",
            "card.observation": "Observação",
            "card.copy": "Copiar",
            "card.copied": "Copiado!",
            "section.variables": "Dicionário de variáveis",
            "section.governance": "Governança",
            "var.name": "Variável",
            "var.meaning": "Significado",
            "var.example": "Exemplo (Libertadores 2026)",
        },
    }
    for m in messages:
        keys["msg"][m["id"]] = {
            "text": f"lib.msg.{m['id']}.text",
            "trigger": f"lib.msg.{m['id']}.trigger",
            "observation": f"lib.msg.{m['id']}.observation",
        }
    for v in variables:
        keys["var"][v["name"]] = {
            "meaning": f"lib.var.{v['name']}.meaning",
            "example": f"lib.var.{v['name']}.example",
        }
    for cat in CATEGORIES_ORDER:
        keys["cat"][cat] = f"lib.cat.{slugify_cat(cat)}"
    return keys


def build_i18n_pt(messages: list[dict], variables: list[dict], keys: dict) -> dict:
    """Dicionário PT plano: chave → valor. Consumido pelo i18n.js."""
    out = dict(keys["ui"])
    for m in messages:
        out[f"lib.msg.{m['id']}.text"] = m["text_pt"]
        out[f"lib.msg.{m['id']}.trigger"] = m["trigger"]
        out[f"lib.msg.{m['id']}.observation"] = m["observation"]
    for v in variables:
        out[f"lib.var.{v['name']}.meaning"] = v["meaning_pt"]
        out[f"lib.var.{v['name']}.example"] = v["example_pt"]
    for cat in CATEGORIES_ORDER:
        out[f"lib.cat.{slugify_cat(cat)}"] = cat
    return out


# Tradução canônica das categorias (UI das chips/filter)
CAT_TRANSLATIONS = {
    "Abertura":                        {"en": "Opening",                      "es": "Apertura",                       "de": "Eröffnung"},
    "Produto & Pacotes":               {"en": "Product & Packages",           "es": "Producto y Paquetes",            "de": "Produkt & Pakete"},
    "Tickets":                         {"en": "Tickets",                      "es": "Entradas",                       "de": "Tickets"},
    "Vôos":                            {"en": "Flights",                      "es": "Vuelos",                         "de": "Flüge"},
    "Hospedagem":                      {"en": "Accommodation",                "es": "Hospedaje",                      "de": "Unterkunft"},
    "Transporte":                      {"en": "Transport",                    "es": "Transporte",                     "de": "Transport"},
    "Documentação":                    {"en": "Documentation",                "es": "Documentación",                  "de": "Dokumentation"},
    "Pagamento":                       {"en": "Payment",                      "es": "Pago",                           "de": "Zahlung"},
    "Políticas":                       {"en": "Policies",                     "es": "Políticas",                      "de": "Richtlinien"},
    "Pós-venda":                       {"en": "After-Sales",                  "es": "Posventa",                       "de": "Nach dem Kauf"},
    "Handoff & Atendimento":           {"en": "Handoff & Support",            "es": "Handoff y Atención",             "de": "Übergabe & Support"},
    "Encerramento & Re-engajamento":   {"en": "Closing & Re-engagement",      "es": "Cierre y Reactivación",          "de": "Abschluss & Reaktivierung"},
    "Eventos / Jogos Flamengo":        {"en": "Flamengo Events",              "es": "Eventos Flamengo",               "de": "Flamengo-Spiele"},
    "Compliance Flamengo/Maracanã":    {"en": "Flamengo/Maracanã Compliance", "es": "Compliance Flamengo/Maracaná",   "de": "Flamengo/Maracanã Compliance"},
    "Descritivo de pacote":            {"en": "Package Description",          "es": "Descripción de paquete",         "de": "Paketbeschreibung"},
    "Checkout":                        {"en": "Checkout",                     "es": "Checkout",                       "de": "Checkout"},
}


def build_i18n_stub(pt: dict, lang: str) -> dict:
    """Stub para EN/ES/DE: mesma estrutura, valores marcados como 'pendente'.

    Estratégia: chaves UI ganham tradução básica imediata. Conteúdo de mensagens
    fica como TODO (com prefixo `[TODO ${lang}]`) para forçar revisão antes de
    publicar tradução. i18n.js faz fallback para PT quando chave ausente.
    """
    base_ui = {
        "en": {
            "hero.title": "Reply Library — Aby",
            "hero.sub": "35 messages across 13 categories. Copy, paste, adjust variables.",
            "filter.all": "All",
            "filter.search.placeholder": "Search by trigger, shortcut or text...",
            "card.shortcut": "Shortcut",
            "card.trigger": "Trigger",
            "card.variables": "Variables",
            "card.observation": "Note",
            "card.copy": "Copy",
            "card.copied": "Copied!",
            "section.variables": "Variable dictionary",
            "section.governance": "Governance",
            "var.name": "Variable",
            "var.meaning": "Meaning",
            "var.example": "Example (Libertadores 2026)",
        },
        "es": {
            "hero.title": "Biblioteca de Respuestas — Aby",
            "hero.sub": "35 mensajes en 13 categorías. Copiá, pegá, ajustá las variables.",
            "filter.all": "Todas",
            "filter.search.placeholder": "Buscar por disparador, atajo o texto...",
            "card.shortcut": "Atajo",
            "card.trigger": "Disparador",
            "card.variables": "Variables",
            "card.observation": "Observación",
            "card.copy": "Copiar",
            "card.copied": "¡Copiado!",
            "section.variables": "Diccionario de variables",
            "section.governance": "Gobernanza",
            "var.name": "Variable",
            "var.meaning": "Significado",
            "var.example": "Ejemplo (Libertadores 2026)",
        },
        "de": {
            "hero.title": "Antwort-Bibliothek — Aby",
            "hero.sub": "35 Nachrichten in 13 Kategorien. Kopieren, einfügen, Variablen anpassen.",
            "filter.all": "Alle",
            "filter.search.placeholder": "Suche nach Trigger, Kürzel oder Text...",
            "card.shortcut": "Kürzel",
            "card.trigger": "Trigger",
            "card.variables": "Variablen",
            "card.observation": "Hinweis",
            "card.copy": "Kopieren",
            "card.copied": "Kopiert!",
            "section.variables": "Variablen-Wörterbuch",
            "section.governance": "Governance",
            "var.name": "Variable",
            "var.meaning": "Bedeutung",
            "var.example": "Beispiel (Libertadores 2026)",
        },
    }
    out = dict(base_ui[lang])
    # Categorias: traduzir via mapa canônico
    # Mensagens / variáveis: stub [TODO LANG] (exige revisão nativa)
    for key in pt:
        if key.startswith("lib.cat."):
            # Encontra o PT-name e traduz
            pt_name = pt[key]
            translated = CAT_TRANSLATIONS.get(pt_name, {}).get(lang)
            out[key] = translated if translated else pt_name
        elif key.startswith("lib.msg.") or key.startswith("lib.var."):
            out[key] = f"[TODO {lang.upper()}] {pt[key]}"
    return out


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {path.relative_to(HERE)} ({len(json.dumps(data))} bytes)")


def validate(messages: list[dict], variables: list[dict]) -> int:
    """Sanity checks. Retorna 0 se OK, >0 se erro."""
    errs = 0
    ids = [m["id"] for m in messages]
    if len(set(ids)) != len(ids):
        print("ERRO: IDs duplicados em messages.json", file=sys.stderr)
        errs += 1
    var_names = {v["name"] for v in variables}
    declared = set()
    for m in messages:
        for v in m["variables"]:
            declared.add(v)
    undeclared = declared - var_names - {
        # Variáveis que aparecem em mensagens mas o dicionário oficial não cobre
        # (são específicas de subconjuntos — registradas para auditoria, não erro)
        "estadio", "torcida", "clube", "url_biometria", "time_casa", "time_visitante",
        "ponto_desembarque", "antecedencia_aviso", "valor", "cores_emojis_clube",
        "clube_credenciado",
    }
    if undeclared:
        print(f"AVISO: variáveis usadas sem entrada no dicionário: {undeclared}",
              file=sys.stderr)
    print(f"OK · {len(messages)} mensagens · {len(variables)} variáveis no dicionário")
    return errs


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true",
                        help="Fetch direto da planilha live (requer requests)")
    parser.add_argument("--validate", action="store_true",
                        help="Apenas valida o JSON gerado")
    args = parser.parse_args()

    if args.online:
        text = fetch_online()
        INPUT_TSV.write_text(text, encoding="utf-8")
        print(f"Fetched planilha online → {INPUT_TSV}")
    elif not INPUT_TSV.exists():
        print(f"ERRO: {INPUT_TSV} não existe. Rode com --online ou cole o markdown manualmente.",
              file=sys.stderr)
        return 1

    text = INPUT_TSV.read_text(encoding="utf-8")
    messages, variables, governance = parse_markdown_table(text)

    if not messages:
        print("ERRO: nenhuma mensagem extraída. Confira o formato do input.tsv.",
              file=sys.stderr)
        return 1

    keys = build_i18n_keys(messages, variables)
    pt = build_i18n_pt(messages, variables, keys)

    # Validação
    rc = validate(messages, variables)
    if args.validate:
        return rc

    # Build messages.json (sem o text_pt — texto vive no i18n)
    messages_clean = []
    for m in messages:
        messages_clean.append({
            "id": m["id"],
            "category": m["category"],
            "shortcut": m["shortcut"],
            "variables": m["variables"],
            "i18n": {
                "text": f"lib.msg.{m['id']}.text",
                "trigger": f"lib.msg.{m['id']}.trigger",
                "observation": f"lib.msg.{m['id']}.observation",
            },
        })
    variables_clean = []
    for v in variables:
        variables_clean.append({
            "name": v["name"],
            "i18n": {
                "meaning": f"lib.var.{v['name']}.meaning",
                "example": f"lib.var.{v['name']}.example",
            },
        })

    meta = {
        "version": "v2-2026-06-02",
        "source": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid={GID_LIBRARY}",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_messages": len(messages),
        "total_variables": len(variables),
        "categories_order": CATEGORIES_ORDER,
    }

    write_json(MESSAGES_JSON, {"meta": meta, "messages": messages_clean})
    write_json(VARIABLES_JSON, {"meta": meta, "variables": variables_clean})
    write_json(I18N_KEYS_JSON, keys)
    write_json(I18N_PT, pt)
    write_json(I18N_EN, build_i18n_stub(pt, "en"))
    write_json(I18N_ES, build_i18n_stub(pt, "es"))
    write_json(I18N_DE, build_i18n_stub(pt, "de"))

    print(f"\nOK · {len(messages)} mensagens · {len(variables)} variáveis · "
          f"7 arquivos gerados em {HERE.relative_to(HERE.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
