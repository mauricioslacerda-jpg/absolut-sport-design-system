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
from datetime import datetime
from pathlib import Path


# Mapa canônico de tradução dos NOMES dos placeholders (legibilidade humana).
# IMPORTANTE: o ManyChat/Aby em produção espera os nomes em PT.
# Placeholders localizados são para leitura/aprendizado por operadores
# não-lusófonos; quando o operador copia a versão localizada, deve
# substituir os {placeholders} pelos valores reais antes de enviar
# (ou usar a versão PT se for alimentar diretamente o bot).
PLACEHOLDER_TRANSLATIONS = {
    # As 13 variáveis do dicionário canônico
    "nome":              {"pt": "nome",              "en": "name",            "es": "nombre",            "de": "name"},
    "atendente":         {"pt": "atendente",         "en": "attendant",       "es": "atendente",         "de": "berater"},
    "parceiro":          {"pt": "parceiro",          "en": "partner",         "es": "socio",             "de": "partner"},
    "evento":            {"pt": "evento",            "en": "event",           "es": "evento",            "de": "event"},
    "cidade":            {"pt": "cidade",            "en": "city",            "es": "ciudad",            "de": "stadt"},
    "data":              {"pt": "data",              "en": "date",            "es": "fecha",             "de": "datum"},
    "url":               {"pt": "url",               "en": "url",             "es": "url",               "de": "url"},
    "origem_aereo":      {"pt": "origem_aereo",      "en": "flight_origin",   "es": "origen_aereo",      "de": "flug_abflug"},
    "pais_prep":         {"pt": "pais_prep",         "en": "country_prep",    "es": "pais_prep",         "de": "land_prep"},
    "doc":               {"pt": "doc",               "en": "doc",             "es": "doc",               "de": "dok"},
    "app_transporte":    {"pt": "app_transporte",    "en": "transport_app",   "es": "app_transporte",    "de": "transport_app"},
    "torcida_alvo":      {"pt": "torcida_alvo",      "en": "target_fanbase",  "es": "hinchada_objetivo", "de": "ziel_fans"},
    "torcida_real":      {"pt": "torcida_real",      "en": "actual_fanbase",  "es": "hinchada_real",     "de": "tatsaechliche_fans"},
    # Variáveis específicas que aparecem em algumas mensagens (Flamengo/Maracanã)
    "estadio":           {"pt": "estadio",           "en": "stadium",         "es": "estadio",           "de": "stadion"},
    "torcida":           {"pt": "torcida",           "en": "fanbase",         "es": "hinchada",          "de": "fangruppe"},
    "clube":             {"pt": "clube",             "en": "club",            "es": "club",              "de": "verein"},
    "url_biometria":     {"pt": "url_biometria",     "en": "biometrics_url",  "es": "url_biometria",     "de": "biometrie_url"},
    "time_casa":         {"pt": "time_casa",         "en": "home_team",       "es": "equipo_local",      "de": "heim_team"},
    "time_visitante":    {"pt": "time_visitante",    "en": "away_team",       "es": "equipo_visitante",  "de": "gast_team"},
    "ponto_desembarque": {"pt": "ponto_desembarque", "en": "drop_off_point",  "es": "punto_desembarque", "de": "ausstieg_punkt"},
    "antecedencia_aviso":{"pt": "antecedencia_aviso","en": "advance_notice",  "es": "antelacion_aviso",  "de": "vorlaufzeit"},
    "valor":             {"pt": "valor",             "en": "price",           "es": "valor",             "de": "preis"},
    "cores_emojis_clube":{"pt": "cores_emojis_clube","en": "club_color_emojis","es": "colores_emojis_club","de": "verein_farben_emojis"},
    "clube_credenciado": {"pt": "clube_credenciado", "en": "accredited_club", "es": "club_acreditado",   "de": "akkreditierter_verein"},
}

_PLACEHOLDER_RE = re.compile(r"\{([\w_]+)\}")


def localize_placeholders(text: str, lang: str) -> str:
    """Substitui {nome} → {name} (etc) conforme o idioma alvo.

    Se uma variável não estiver mapeada, mantém o nome original
    (evita quebra silenciosa). PT é no-op.
    """
    if lang == "pt":
        return text
    def repl(m):
        var = m.group(1)
        tr = PLACEHOLDER_TRANSLATIONS.get(var, {}).get(lang)
        return "{" + (tr if tr else var) + "}"
    return _PLACEHOLDER_RE.sub(repl, text)


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
            "gov.contract.title":     "Texto contratual",
            "gov.contract.body":      "A mensagem A20 (Política de cancelamento) é texto contratual. Não alterar sem revisão jurídica.",
            "gov.inventory.title":    "Inventário",
            "gov.inventory.body":     "As mensagens de inventário (voos, hotel, camarote) assumem \"esgotado\". Revisar a cada evento conforme estoque real.",
            "gov.aby.title":          "Ligação com a Aby",
            "gov.aby.body":           "A24, A25, A26 e A28 correspondem aos itens 01/03, 31, 04 e 32 da auditoria do bot. Esta copy é a fonte canônica.",
            "gov.reuse.title":        "Reuso por evento",
            "gov.reuse.body":         "Para um novo evento, basta reescrever o dicionário de variáveis. A copy serve a qualquer evento.",
            "gov.placeholders.title": "⚠️ Placeholders localizados",
            "gov.placeholders.body":  "Os placeholders ({name}, {nombre}, {berater}) são localizados para leitura humana. O ManyChat/Aby em produção só entende a versão PT ({nome}, {atendente}). Se for alimentar o bot, copie a versão PT. Se for usar manualmente, substitua os placeholders pelos valores reais antes de enviar.",
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


# Tradução canônica das 13 variáveis (dicionário)
# meaning: tradução funcional obrigatória
# example: traduzido onde fizer sentido (frases descritivas);
#          mantido em PT para nomes próprios e valores literais
VAR_TRANSLATIONS = {
    "nome": {
        "label":   {"pt": "Nome do cliente",      "en": "Customer name",        "es": "Nombre del cliente",   "de": "Kundenname"},
        "meaning": {"en": "Customer/fan name",
                    "es": "Nombre del cliente/hincha",
                    "de": "Name des Kunden/Fans"},
        "example": {"en": "João", "es": "João", "de": "João"},
    },
    "atendente": {
        "label":   {"pt": "Atendente",            "en": "Attendant",            "es": "Atendente",            "de": "Berater"},
        "meaning": {"en": "Attendant / campaign persona name",
                    "es": "Nombre del atendente / persona de la campaña",
                    "de": "Name des Beraters / der Kampagnen-Persona"},
        "example": {"en": "Thadeu", "es": "Thadeu", "de": "Thadeu"},
    },
    "parceiro": {
        "label":   {"pt": "Parceiro oficial",     "en": "Official partner",     "es": "Socio oficial",        "de": "Offizieller Partner"},
        "meaning": {"en": "Official rights-holding entity",
                    "es": "Entidad oficial titular de los derechos",
                    "de": "Offizielle Rechteinhaberin"},
        "example": {"en": "CONMEBOL", "es": "CONMEBOL", "de": "CONMEBOL"},
    },
    "evento": {
        "label":   {"pt": "Evento",               "en": "Event",                "es": "Evento",               "de": "Event"},
        "meaning": {"en": "Event name (as told to the customer)",
                    "es": "Nombre del evento (tal como se le dice al cliente)",
                    "de": "Eventname (wie dem Kunden mitgeteilt)"},
        "example": {"en": "the Glória Eterna grand final",
                    "es": "la gran final de la Glória Eterna",
                    "de": "das große Finale der Glória Eterna"},
    },
    "cidade": {
        "label":   {"pt": "Cidade-sede",          "en": "Host city",            "es": "Ciudad-sede",          "de": "Austragungsort"},
        "meaning": {"en": "Host city of the event",
                    "es": "Ciudad-sede del evento",
                    "de": "Austragungsort des Events"},
        "example": {"en": "Lima", "es": "Lima", "de": "Lima"},
    },
    "data": {
        "label":   {"pt": "Data do evento",       "en": "Event date",           "es": "Fecha del evento",     "de": "Eventdatum"},
        "meaning": {"en": "Event date (day or full date)",
                    "es": "Fecha del evento (día o fecha completa)",
                    "de": "Eventdatum (Tag oder Volldatum)"},
        "example": {"en": "29", "es": "29", "de": "29"},
    },
    "url": {
        "label":   {"pt": "Link do e-commerce",   "en": "E-commerce link",      "es": "Enlace e-commerce",    "de": "E-Commerce-Link"},
        "meaning": {"en": "Event e-commerce link",
                    "es": "Enlace del e-commerce del evento",
                    "de": "E-Commerce-Link des Events"},
        "example": {"en": "absolutsport.com.br/palmeiraslibertadores",
                    "es": "absolutsport.com.br/palmeiraslibertadores",
                    "de": "absolutsport.com.br/palmeiraslibertadores"},
    },
    "origem_aereo": {
        "label":   {"pt": "Origem aérea",         "en": "Flight origin",        "es": "Salida aérea",         "de": "Flug-Abflug"},
        "meaning": {"en": "Available flight departure cities",
                    "es": "Plazas de salida del vuelo disponible",
                    "de": "Verfügbare Flug-Abflugorte"},
        "example": {"en": "São Paulo and Rio de Janeiro",
                    "es": "São Paulo y Río de Janeiro",
                    "de": "São Paulo und Rio de Janeiro"},
    },
    "pais_prep": {
        "label":   {"pt": "País + preposição",    "en": "Country + preposition", "es": "País + preposición",  "de": "Land + Präposition"},
        "meaning": {"en": "Destination country with preposition",
                    "es": "País-destino con preposición",
                    "de": "Zielland mit Präposition"},
        "example": {"en": "in Peru", "es": "en Perú", "de": "in Peru"},
    },
    "doc": {
        "label":   {"pt": "Documento",            "en": "Document",             "es": "Documento",            "de": "Dokument"},
        "meaning": {"en": "Documents accepted for entry",
                    "es": "Documentos aceptados para la entrada",
                    "de": "Für die Einreise akzeptierte Dokumente"},
        "example": {"en": "ID or Passport",
                    "es": "Cédula o Pasaporte",
                    "de": "Personalausweis oder Reisepass"},
    },
    "app_transporte": {
        "label":   {"pt": "App de transporte",    "en": "Transport app",        "es": "App de transporte",    "de": "Transport-App"},
        "meaning": {"en": "Recommended ride-hailing app at the destination",
                    "es": "App de transporte recomendada en el destino",
                    "de": "Empfohlene Transport-App am Reiseziel"},
        "example": {"en": "Uber", "es": "Uber", "de": "Uber"},
    },
    "torcida_alvo": {
        "label":   {"pt": "Torcida alvo",         "en": "Target fanbase",       "es": "Hinchada objetivo",    "de": "Ziel-Fangruppe"},
        "meaning": {"en": "Target fanbase of the acquisition campaign",
                    "es": "Hinchada objetivo de la campaña de captación",
                    "de": "Ziel-Fangruppe der Akquisekampagne"},
        "example": {"en": "Palmeiras fans",
                    "es": "hinchas palmeirenses",
                    "de": "Palmeiras-Fans"},
    },
    "torcida_real": {
        "label":   {"pt": "Torcida real",         "en": "Actual fanbase",       "es": "Hinchada real",        "de": "Tatsächliche Fangruppe"},
        "meaning": {"en": "Customer's actual fanbase (record correction)",
                    "es": "Hinchada real del cliente (corrección de registro)",
                    "de": "Tatsächliche Fangruppe des Kunden (Datensatz-Korrektur)"},
        "example": {"en": "Flamengo fan",
                    "es": "hincha flamenguista",
                    "de": "Flamengo-Fan"},
    },
}


# Tradução canônica das 35 mensagens (trigger + text + observation).
# Placeholders {nome}, {url}, etc. NUNCA são traduzidos — são substituídos
# em runtime pelo ManyChat/Aby.
MSG_TRANSLATIONS = {
    "A01": {
        "trigger": {"en": "First contact / greeting", "es": "Primer contacto / saludo", "de": "Erstkontakt / Begrüßung"},
        "text": {
            "en": "Hi, {nome}! Great to talk with you. This is {atendente}, from the ABSOLUT Sport Sales team — the first and only Official Travel Agency of {parceiro}! It will be a pleasure to help you experience {evento}, in {cidade}, on {data}! All package options are on our website {url} and may include flights, accommodation, ground transport, on-site support and, of course, tickets. Packages are limited and stock is in the final stretch — hurry and secure yours!",
            "es": "¡Hola, {nome}! Un gusto hablar con vos. Soy {atendente}, del equipo de Ventas de ABSOLUT Sport, la primera y única Agencia de Viajes Oficial de {parceiro}! Va a ser un placer ayudarte a vivir {evento}, en {cidade}, el día {data}! Todas las opciones de paquete están en nuestro sitio {url} y pueden incluir transporte aéreo, alojamiento, transporte terrestre, asistencia in-situ y, claro, entradas. Los paquetes son limitados y ya están en la recta final de stock — ¡apurate y asegurá el tuyo!",
            "de": "Hallo, {nome}! Schön, mit dir zu sprechen. Hier ist {atendente} vom Verkaufsteam von ABSOLUT Sport, dem ersten und einzigen offiziellen Reisebüro von {parceiro}! Es wird mir eine Freude sein, dich {evento}, in {cidade}, am {data} erleben zu lassen! Alle Paket-Optionen findest du auf unserer Website {url} und können Flug, Unterkunft, Transport vor Ort, Vor-Ort-Betreuung und natürlich Tickets enthalten. Die Pakete sind begrenzt und der Bestand neigt sich dem Ende zu — sichere dir schnell deins!",
        },
        "observation": {"en": "Adjust greeting (Good morning/afternoon/evening) according to time of day.", "es": "Ajustar saludo (Buenos días/Buenas tardes/Buenas noches) según horario.", "de": "Begrüßung (Guten Morgen / Guten Tag / Guten Abend) je nach Tageszeit anpassen."},
    },
    "A02": {
        "trigger": {"en": "What's included / personalize (flight from another city)", "es": "Qué incluye / personalizar (vuelo desde otra ciudad)", "de": "Was ist enthalten / anpassen (Flug aus anderer Stadt)"},
        "text": {
            "en": "All package options are on the website {url} and may include flights, accommodation, ground transport, on-site support and tickets. Flights depart exclusively from {origem_aereo}; flights from other cities are sold out.",
            "es": "Todas las opciones de paquete están en el sitio {url} y pueden incluir transporte aéreo, alojamiento, transporte terrestre, asistencia in-situ y entradas. Las salidas aéreas son exclusivamente desde {origem_aereo}; los vuelos desde otras plazas ya están agotados.",
            "de": "Alle Paket-Optionen findest du auf der Website {url} und können Flug, Unterkunft, Transport vor Ort, Vor-Ort-Betreuung und Tickets enthalten. Flüge starten ausschließlich aus {origem_aereo}; Flüge aus anderen Städten sind bereits ausverkauft.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A03": {
        "trigger": {"en": "How much does package X cost", "es": "Cuánto cuesta el paquete X", "de": "Was kostet Paket X"},
        "text": {
            "en": "All options are on the website {url}. The final price is calculated on the platform itself, according to the hospitality options chosen.",
            "es": "Todas las opciones están en el sitio {url}. El precio final se calcula en la propia plataforma, según las opciones de hospitalidad elegidas.",
            "de": "Alle Optionen findest du auf der Website {url}. Der Endpreis wird direkt auf der Plattform berechnet, je nach gewählten Hospitality-Optionen.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A04": {
        "trigger": {"en": "Can I negotiate a discount?", "es": "¿Puedo negociar descuento?", "de": "Kann ich einen Rabatt verhandeln?"},
        "text": {
            "en": "{nome}, at this stage of the sales cycle all packages have fixed composition and price, available exclusively online on our e-commerce. All available options are at {url}. I'm here for any questions.",
            "es": "{nome}, en este momento del ciclo de ventas todos los paquetes tienen composición y precio cerrados, habilitados para venta exclusiva online en nuestro e-commerce. Todas las opciones disponibles están en {url}. Quedo a disposición para dudas.",
            "de": "{nome}, in dieser Phase des Verkaufszyklus haben alle Pakete eine festgelegte Zusammensetzung und einen festen Preis und sind ausschließlich online in unserem E-Commerce erhältlich. Alle verfügbaren Optionen findest du unter {url}. Ich stehe gerne für Fragen zur Verfügung.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A05": {
        "trigger": {"en": "Price defense (complaint)", "es": "Defensa del precio (queja)", "de": "Preisverteidigung (Beschwerde)"},
        "text": {
            "en": "It's important to highlight that our pricing follows reasonable margins, within market standards, and includes — besides the hospitality services — the entire on-site Agency operation, support team, taxes, license fees and royalties paid to {parceiro} as Official Agency, plus other operational costs of the project.",
            "es": "Es importante destacar que nuestra precificación sigue márgenes razonables, dentro de lo practicado en el mercado, e incluye — además de los servicios de hospitalidad — toda la operación de la Agencia in-situ, equipo de soporte, carga tributaria, tasa de licencia y royalties pagados a {parceiro} como Agencia Oficial, además de otros costos operativos del proyecto.",
            "de": "Wichtig zu betonen: Unsere Preisgestaltung folgt angemessenen Margen im marktüblichen Rahmen und umfasst — neben den Hospitality-Leistungen — den gesamten Agentur-Betrieb vor Ort, das Support-Team, Steuern, Lizenzgebühren und Royalties an {parceiro} als offizielle Agentur, sowie weitere operative Projektkosten.",
        },
        "observation": {"en": "Use only if the customer complains about the price.", "es": "Usar sólo si el cliente se queja del precio.", "de": "Nur verwenden, wenn der Kunde sich über den Preis beschwert."},
    },
    "A06": {
        "trigger": {"en": "Exclusive fan section / do you have CAT3?", "es": "Hinchada exclusiva / ¿tienen CAT3?", "de": "Fan-Sektor exklusiv / habt ihr CAT3?"},
        "text": {
            "en": "Unfortunately no. As Official Agency of {parceiro}, the partnership scope only includes packages with CAT1 or CAT2 tickets, plus Hospitality zone passes. All our tickets are for mixed sectors. The exclusive sectors for each fanbase (CAT3) are sold directly by {parceiro} and the finalist clubs. Packages available at {url}.",
            "es": "Lamentablemente no. Como Agencia Oficial de {parceiro}, el alcance de la asociación incluye sólo paquetes con entradas CAT1 o CAT2, además de pases para la zona de Hospitalidad. Todas nuestras entradas son para sectores mixtos. Los sectores exclusivos de cada hinchada (CAT3) son comercializados directamente por {parceiro} y los clubes finalistas. Paquetes disponibles en {url}.",
            "de": "Leider nein. Als offizielle Agentur von {parceiro} umfasst der Partnerschafts-Umfang nur Pakete mit CAT1- oder CAT2-Tickets sowie Pässe für die Hospitality-Zone. Alle unsere Tickets sind für gemischte Sektoren. Die exklusiven Sektoren pro Fanlager (CAT3) werden direkt von {parceiro} und den Finalisten-Clubs verkauft. Pakete verfügbar unter {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A07": {
        "trigger": {"en": "Difference between CAT1 and CAT2", "es": "Diferencia entre CAT1 y CAT2", "de": "Unterschied zwischen CAT1 und CAT2"},
        "text": {
            "en": "Both categories are in central sectors with mixed fans. The difference is in the view of the awards ceremony: CAT1 (west) offers a frontal view of the stage and the trophy presentation; CAT2 (east) is on the other side of the stadium. Last units at {url}.",
            "es": "Las dos categorías están en sectores centrales con hinchada mixta. La diferencia está en la vista de la ceremonia de premiación: la CAT1 (occidente) ofrece vista frontal del palco y la entrega del trofeo; la CAT2 (oriente) queda del otro lado del estadio. Últimas unidades en {url}.",
            "de": "Beide Kategorien befinden sich in zentralen Sektoren mit gemischten Fans. Der Unterschied liegt in der Sicht auf die Siegerehrung: CAT1 (West) bietet einen frontalen Blick auf die Bühne und die Trophäen-Übergabe; CAT2 (Ost) liegt auf der anderen Seite des Stadions. Letzte Einheiten unter {url}.",
        },
        "observation": {"en": "Adjust sector names according to the event venue.", "es": "Ajustar nombres de sector según el estadio del evento.", "de": "Sektor-Bezeichnungen je nach Stadion des Events anpassen."},
    },
    "A08": {
        "trigger": {"en": "What is Hospitality?", "es": "¿Qué es el Hospitality?", "de": "Was ist Hospitality?"},
        "text": {
            "en": "It's a premium experience that combines the ticket with access to a VIP area: open bar, open food, sponsor activations, VIP guests, big screens, climate-controlled lounges and other attractions. Hospitality packages include CAT ticket. Last units at {url}.",
            "es": "Es una experiencia premium que combina la entrada con acceso a un área VIP: open bar, open food, activaciones de patrocinadores, invitados VIP, pantallas, lounges climatizados y otras atracciones. Los paquetes de hospitalidad incluyen entrada CAT. Últimas unidades en {url}.",
            "de": "Es ist ein Premium-Erlebnis, das das Ticket mit Zugang zu einem VIP-Bereich kombiniert: Open Bar, Open Food, Sponsoren-Aktivierungen, VIP-Gäste, Großbildschirme, klimatisierte Lounges und andere Attraktionen. Hospitality-Pakete enthalten ein CAT-Ticket. Letzte Einheiten unter {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A09": {
        "trigger": {"en": "Do you have private boxes?", "es": "¿Tienen palco?", "de": "Habt ihr Logen?"},
        "text": {
            "en": "Unfortunately our private box stock is sold out, {nome}! If anything new comes up, we'll let you know. The entire inventory of still-available packages is at {url}.",
            "es": "Lamentablemente nuestro stock de palcos está agotado, {nome}! En caso de novedades, te informaremos. Todo el inventario de paquetes aún disponibles está en {url}.",
            "de": "Leider ist unser Logen-Bestand ausverkauft, {nome}! Sollte sich etwas ändern, geben wir Bescheid. Das gesamte Inventar noch verfügbarer Pakete findest du unter {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A10": {
        "trigger": {"en": "Half-price ticket / free admission?", "es": "¿Existe media entrada / gratuidad?", "de": "Gibt es ermäßigte Tickets / Freikarten?"},
        "text": {
            "en": "{parceiro}'s ticket policy does not provide for half-price tickets or free admission for any audience. In compliance, as Official Partner, our packages follow the same guideline.",
            "es": "La política de entradas de {parceiro} no prevé media entrada ni gratuidad para ningún público. En conformidad, como Socia Oficial, nuestros paquetes siguen la misma directriz.",
            "de": "Die Ticket-Richtlinie von {parceiro} sieht weder ermäßigte Tickets noch Freikarten für irgendeine Zielgruppe vor. Als offizieller Partner folgen unsere Pakete derselben Richtlinie.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A11": {
        "trigger": {"en": "Any other flight options?", "es": "¿Tienen otras opciones de vuelos?", "de": "Gibt es andere Flugoptionen?"},
        "text": {
            "en": "{nome}, demand is very high and some flight and accommodation options are already sold out. All available options are on the website {url}.",
            "es": "{nome}, la demanda está muy alta y algunas opciones de vuelo y alojamiento ya se agotaron. Todas las opciones disponibles están en el sitio {url}.",
            "de": "{nome}, die Nachfrage ist sehr hoch und einige Flug- und Unterkunftsoptionen sind bereits ausverkauft. Alle verfügbaren Optionen findest du auf der Website {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A12": {
        "trigger": {"en": "Move up / customize flight", "es": "Anticipar / personalizar vuelo", "de": "Flug vorziehen / individualisieren"},
        "text": {
            "en": "Unfortunately no, {nome}. Our direct agreements with airlines do not allow changes to the contracted route. All still-available options, departing from {origem_aereo}, are on the e-commerce {url}.",
            "es": "Lamentablemente no, {nome}. Nuestros acuerdos directos con las aerolíneas no permiten alteración en la malla contratada. Todas las opciones aún disponibles, saliendo de {origem_aereo}, están en el e-commerce {url}.",
            "de": "Leider nein, {nome}. Unsere Direktvereinbarungen mit den Fluggesellschaften erlauben keine Änderung am gebuchten Streckennetz. Alle noch verfügbaren Optionen ab {origem_aereo} findest du im E-Commerce {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A13": {
        "trigger": {"en": "Can I buy only the flight?", "es": "¿Puedo comprar sólo el aéreo?", "de": "Kann ich nur den Flug kaufen?"},
        "text": {
            "en": "Hi, {nome}. We are not authorized by {parceiro} to sell standalone services. Flight packages are offered only together with the other hospitality services, available at {url}.",
            "es": "Hola, {nome}. No estamos autorizados por {parceiro} a vender servicios sueltos. Los paquetes con aéreo se ofrecen sólo en conjunto con los demás servicios de hospitalidad, disponibles en {url}.",
            "de": "Hallo, {nome}. Wir sind von {parceiro} nicht autorisiert, einzelne Leistungen zu verkaufen. Pakete mit Flug werden ausschließlich zusammen mit den anderen Hospitality-Leistungen angeboten, verfügbar unter {url}.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A14": {
        "trigger": {"en": "Triple room (TRP)?", "es": "¿Habitación triple (TRP)?", "de": "Dreibettzimmer (TRP)?"},
        "text": {
            "en": "Our triple room availability is quite limited and the entire inventory has been consumed. If new availability or cancellations come up, inventory returns for sale at {url}.",
            "es": "Nuestra disponibilidad de habitaciones triples es bastante limitada y todo el inventario ya fue consumido. Si hay nuevas disponibilidades o cancelaciones, el inventario vuelve para venta en {url}.",
            "de": "Unsere Verfügbarkeit an Dreibettzimmern ist sehr begrenzt und der gesamte Bestand ist aufgebraucht. Sollten neue Verfügbarkeiten oder Stornierungen eintreten, kehrt das Inventar zum Verkauf unter {url} zurück.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A15": {
        "trigger": {"en": "Extra nights?", "es": "¿Noches extra?", "de": "Extra-Nächte?"},
        "text": {
            "en": "At this moment, the contracted hotels have used up their entire extra-nights inventory. If new availability or cancellations come up, they return for sale at {url}.",
            "es": "En este momento, los hoteles bloqueados tienen todo el inventario de noches extras consumido. Si hay nuevas disponibilidades o cancelaciones, vuelve para venta en {url}.",
            "de": "Aktuell ist der gesamte Bestand an Extra-Nächten in den reservierten Hotels aufgebraucht. Sollten neue Verfügbarkeiten oder Stornierungen eintreten, kehrt das Angebot zum Verkauf unter {url} zurück.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A16": {
        "trigger": {"en": "Airport transfer?", "es": "¿Transfer en el aeropuerto?", "de": "Flughafen-Transfer?"},
        "text": {
            "en": "{nome}, to ensure full compliance with our service standard, in this edition in {cidade} we will not work with Transfer-In/Transfer-Out (airport–hotel). The airport has a taxi rank and easy access to {app_transporte}, the ride-hailing app we recommend in {cidade}.",
            "es": "{nome}, para garantizar conformidad plena con nuestro estándar de servicio, en esta edición en {cidade} no trabajaremos con Transfer-In/Transfer-Out (aeropuerto–hotel). El aeropuerto tiene parada de taxis y acceso fácil a {app_transporte}, app de transporte que recomendamos en {cidade}.",
            "de": "{nome}, um die volle Einhaltung unseres Servicestandards zu gewährleisten, arbeiten wir in dieser Ausgabe in {cidade} nicht mit Transfer-In/Transfer-Out (Flughafen–Hotel). Der Flughafen bietet Taxistände und einfachen Zugang zu {app_transporte}, der Transport-App, die wir in {cidade} empfehlen.",
        },
        "observation": {"en": "Adjust transfer policy according to the edition.", "es": "Ajustar política de transfer según la edición.", "de": "Transfer-Richtlinie je nach Ausgabe anpassen."},
    },
    "A17": {
        "trigger": {"en": "Do I need a passport?", "es": "¿Necesita pasaporte?", "de": "Brauche ich einen Reisepass?"},
        "text": {
            "en": "To enter {pais_prep}, you must present {doc} (within validity), with photo and in good condition.",
            "es": "Para entrar {pais_prep}, es necesario presentar {doc} (dentro de la validez), con foto y en buen estado de conservación.",
            "de": "Zur Einreise {pais_prep} ist die Vorlage von {doc} (gültig), mit Foto und in gutem Zustand erforderlich.",
        },
        "observation": {"en": "Check visa/document requirements per country for each event.", "es": "Verificar exigencia de visa/documento por país en cada evento.", "de": "Visa-/Dokumentenanforderung pro Land bei jedem Event prüfen."},
    },
    "A18": {
        "trigger": {"en": "When do I receive the official info?", "es": "¿Cuándo recibo la información oficial?", "de": "Wann erhalte ich die offiziellen Infos?"},
        "text": {
            "en": "In the coming days our after-sales team will get in touch with all the details of your trip, including vouchers and official schedules. Information for each service (ticketing, accommodation, flight) is sent at most 2 days before use.",
            "es": "En los próximos días nuestro equipo de posventa entrará en contacto con todos los detalles de tu viaje, incluyendo vouchers y horarios oficiales. La información de cada servicio (ticketing, alojamiento, aéreo) se envía con un máximo de 2 días de antelación al uso.",
            "de": "In den kommenden Tagen meldet sich unser After-Sales-Team mit allen Details deiner Reise, einschließlich Vouchers und offizieller Zeitpläne. Die Informationen zu jedem Service (Ticketing, Unterkunft, Flug) werden spätestens 2 Tage vor der Nutzung versandt.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A19": {
        "trigger": {"en": "Payment methods", "es": "Formas de pago", "de": "Zahlungsmethoden"},
        "text": {
            "en": "Our website accepts PIX — with 10% off! — and credit card (up to 5x interest-free or up to 10x with interest). All payment methods and available packages are at {url}.",
            "es": "Nuestro sitio acepta PIX — ¡con 10% de descuento! — y tarjeta de crédito (hasta 5 cuotas sin interés o hasta 10 con interés). Todos los medios y paquetes disponibles están en {url}.",
            "de": "Unsere Website akzeptiert PIX — mit 10% Rabatt! — und Kreditkarte (bis 5x zinsfrei oder bis 10x mit Zinsen). Alle Zahlungsmethoden und verfügbaren Pakete findest du unter {url}.",
        },
        "observation": {"en": "Check current installment/discount conditions.", "es": "Verificar condiciones de cuotas/descuento vigentes.", "de": "Aktuelle Raten-/Rabatt-Bedingungen prüfen."},
    },
    "A20": {
        "trigger": {"en": "Cancellation policy", "es": "Política de cancelación", "de": "Stornierungsrichtlinie"},
        "text": {
            "en": "Our policy provides full refund for cancellations within 7 days of purchase, except for purchases made less than 7 days before the event (no refund). After 7 days of purchase, ABSOLUT retains 80% of the value and converts 20% into ABSOLUT Sport Credits, usable on other products within 1 year of purchase.",
            "es": "Nuestra política prevé reembolso íntegro para cancelaciones dentro de 7 días de la compra, salvo compras realizadas a menos de 7 días del evento (sin reembolso). Después de 7 días de la compra, ABSOLUT retiene el 80% del valor y revierte el 20% en Créditos ABSOLUT Sport, utilizables en otros productos en un plazo de 1 año desde la compra.",
            "de": "Unsere Richtlinie sieht volle Rückerstattung für Stornierungen innerhalb von 7 Tagen nach dem Kauf vor, außer bei Käufen weniger als 7 Tage vor dem Event (keine Rückerstattung). Nach 7 Tagen Kauf behält ABSOLUT 80% des Betrags ein und wandelt 20% in ABSOLUT Sport Credits um, einsetzbar auf andere Produkte innerhalb von 1 Jahr nach dem Kauf.",
        },
        "observation": {"en": "CONTRACTUAL TEXT — do not alter without legal review.", "es": "TEXTO CONTRACTUAL — no alterar sin revisión jurídica.", "de": "VERTRAGSTEXT — nicht ohne juristische Prüfung ändern."},
    },
    "A21": {
        "trigger": {"en": "What happens if the venue changes?", "es": "¿Qué pasa en caso de cambio de sede?", "de": "Was passiert bei einem Veranstaltungsortwechsel?"},
        "text": {
            "en": "As Official Agency of {parceiro}, our operation is not based on rumors. We work with the official information that the event is confirmed and held in {cidade}. Should concrete news of a venue change arise, we will inform each customer.",
            "es": "Como Agencia Oficial de {parceiro}, nuestra operación no se basa en rumores. Trabajamos con la información oficial de que el evento está confirmado y mantenido en {cidade}. Si hay novedad concreta sobre cambio de sede, informaremos a cada cliente.",
            "de": "Als offizielle Agentur von {parceiro} basiert unser Betrieb nicht auf Gerüchten. Wir arbeiten mit der offiziellen Information, dass das Event bestätigt ist und in {cidade} stattfindet. Sollte es konkrete Neuigkeiten zu einem Ortswechsel geben, informieren wir jeden Kunden.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A22": {
        "trigger": {"en": "Already purchased (thank for trust)", "es": "Ya compré (agradecer confianza)", "de": "Bereits gekauft (Vertrauen danken)"},
        "text": {
            "en": "Thank you for your trust, {nome}! We are at your disposal for any support. Stay tuned to our social media and email communications to follow the preparations.",
            "es": "¡Agradecemos la confianza, {nome}! Quedamos a disposición para cualquier soporte. Mantente atento a nuestras redes y comunicaciones por e-mail para acompañar los preparativos.",
            "de": "Danke für dein Vertrauen, {nome}! Wir stehen für jeglichen Support zur Verfügung. Bleib unseren Social Media und E-Mail-Kommunikationen treu, um die Vorbereitungen zu verfolgen.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A23": {
        "trigger": {"en": "Already purchased — how do I receive confirmations?", "es": "Ya compré — ¿cómo recibo las confirmaciones?", "de": "Bereits gekauft — wie erhalte ich Bestätigungen?"},
        "text": {
            "en": "Thank you for your trust, {nome}! Can you confirm if you received our confirmation message by email? Stay tuned to your inbox and our social media. Our support team will be in touch to ensure you receive all the information for the contracted services.",
            "es": "¡Agradecemos la confianza, {nome}! ¿Podés confirmar si recibiste nuestro mensaje de confirmación por e-mail? Mantente atento a la bandeja de entrada y a las redes. Nuestro equipo de atención entrará en contacto para asegurar la recepción de toda la información de los servicios contratados.",
            "de": "Danke für dein Vertrauen, {nome}! Kannst du bestätigen, ob du unsere Bestätigungsnachricht per E-Mail erhalten hast? Behalte deinen Posteingang und unsere Social Media im Auge. Unser Support-Team meldet sich, um den Erhalt aller Informationen zu den gebuchten Leistungen sicherzustellen.",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A24": {
        "trigger": {"en": "Can I talk to a human?", "es": "¿Puedo hablar con un humano?", "de": "Kann ich mit einem Menschen sprechen?"},
        "text": {
            "en": "{nome}, all package options are on the website {url}! If you'd like to talk to an attendant, let me know and I'll add you to the waiting list — someone will get in touch as soon as possible. At the moment we have many requests in the central, so I recommend the website, where the purchase is fast, secure and complete.",
            "es": "{nome}, ¡todas las opciones de paquete están en el sitio {url}! Si querés hablar con un atendente, avisame y te incluyo en la lista de espera — apenas posible alguien entra en contacto. En este momento estamos con muchos llamados en la central, por eso recomiendo el sitio, donde la compra es rápida, segura y completa.",
            "de": "{nome}, alle Paket-Optionen findest du auf der Website {url}! Wenn du mit einem Berater sprechen möchtest, sag mir Bescheid und ich setze dich auf die Warteliste — sobald wie möglich meldet sich jemand. Aktuell haben wir viele Anfragen in der Zentrale, deshalb empfehle ich die Website, wo der Kauf schnell, sicher und vollständig ist.",
        },
        "observation": {"en": "Related to items 01/03 of the Aby audit (human handoff).", "es": "Relacionado a los ítems 01/03 de la auditoría Aby (handoff humano).", "de": "Bezogen auf Punkte 01/03 des Aby-Audits (Human-Handoff)."},
    },
    "A25": {
        "trigger": {"en": "Flooded support (understanding for patience)", "es": "Atención floodada (comprensión por la paciencia)", "de": "Überlastete Betreuung (Verständnis für Geduld)"},
        "text": {
            "en": "I'm finishing up another conversation and I'll get back to you as soon as possible! In the meantime, is there any question I can move forward? Let me know and I or someone from the support team will get in touch.",
            "es": "¡Estoy finalizando una atención y te respondo apenas posible! Mientras tanto, ¿tenés alguna duda que pueda adelantar? Avisame y yo o alguien del equipo de soporte entra en contacto.",
            "de": "Ich beende gerade einen Vorgang und melde mich so schnell wie möglich zurück! In der Zwischenzeit: Gibt es eine Frage, die ich vorab klären kann? Sag Bescheid und ich oder jemand vom Support-Team meldet sich.",
        },
        "observation": {"en": "Related to item 31 of the audit (use of queue time).", "es": "Relacionado al ítem 31 de la auditoría (uso del tiempo de cola).", "de": "Bezogen auf Punkt 31 des Audits (Nutzung der Wartezeit)."},
    },
    "A26": {
        "trigger": {"en": "Buy time (no ready answer)", "es": "Ganar tiempo (sin respuesta lista)", "de": "Zeit gewinnen (keine vorgefertigte Antwort)"},
        "text": {
            "en": "{nome}, I'll confirm this information with my Operations team and get back to you as soon as possible, OK?",
            "es": "{nome}, voy a confirmar esa información con mi equipo de Operaciones y vuelvo apenas posible, ¿OK?",
            "de": "{nome}, ich kläre diese Information mit meinem Operations-Team und melde mich so schnell wie möglich zurück, OK?",
        },
        "observation": {"en": "Related to item 04 of the audit (graceful fallback).", "es": "Relacionado al ítem 04 de la auditoría (fallback gracioso).", "de": "Bezogen auf Punkt 04 des Audits (anmutiges Fallback)."},
    },
    "A27": {
        "trigger": {"en": "Thank for consultation (didn't buy)", "es": "Agradecer consulta (no compró)", "de": "Anfrage danken (kein Kauf)"},
        "text": {
            "en": "Thanks for the consultation, {nome}! We are at your disposal for questions and if you'd like to resume the conversation. Cheers!",
            "es": "¡Agradezco la consulta, {nome}! Quedamos a disposición para dudas y por si querés retomar la atención. ¡Un abrazo!",
            "de": "Danke für die Anfrage, {nome}! Wir stehen für Fragen zur Verfügung und falls du das Gespräch wieder aufnehmen möchtest. Liebe Grüße!",
        },
        "observation": {"en": "", "es": "", "de": ""},
    },
    "A28": {
        "trigger": {"en": "Ghosting / closure due to inactivity", "es": "Ghosting / cierre por inactividad", "de": "Ghosting / Abschluss wegen Inaktivität"},
        "text": {
            "en": "Due to inactivity, this conversation is being closed. But if any question comes up or if you need help to close your package to {cidade} or any other event, I'll be at your disposal to secure your spot in this unique experience!",
            "es": "Debido a la inactividad, esta atención está siendo cerrada. Pero si surge cualquier duda o si necesitás ayuda para cerrar tu paquete rumbo a {cidade} o cualquier otro evento, estaré a disposición para garantizar tu lugar en esa experiencia única!",
            "de": "Aufgrund von Inaktivität wird dieser Vorgang geschlossen. Aber sollte eine Frage aufkommen oder solltest du Hilfe brauchen, um dein Paket nach {cidade} oder zu einem anderen Event abzuschließen, stehe ich zur Verfügung, um dir deinen Platz bei diesem einzigartigen Erlebnis zu sichern!",
        },
        "observation": {"en": "Related to item 32 of the audit (explicit closure).", "es": "Relacionado al ítem 32 de la auditoría (cierre explícito).", "de": "Bezogen auf Punkt 32 des Audits (expliziter Abschluss)."},
    },
    "A29": {
        "trigger": {"en": "Apologize (not from the campaign's fanbase)", "es": "Pedir disculpas (no es de la hinchada de la campaña)", "de": "Sich entschuldigen (nicht aus der Kampagnen-Fangruppe)"},
        "text": {
            "en": "Hey, {nome}! Thanks for understanding and I apologize for the slip. My number is on a specific campaign with {torcida_alvo} fans, in partnership with an influencer. I've already registered you here as {torcida_real} so I don't slip up again!",
            "es": "¡Eh, {nome}! Agradezco la comprensión y pido disculpas por el desliz. Mi número está en una campaña específica con hinchas {torcida_alvo}, en alianza con un influencer. Ya te registré acá como {torcida_real} para no vacilar de nuevo!",
            "de": "Hey, {nome}! Danke fürs Verständnis und entschuldige den Patzer. Meine Nummer läuft in einer spezifischen Kampagne mit {torcida_alvo}-Fans, in Partnerschaft mit einem Influencer. Ich habe dich hier schon als {torcida_real} registriert, damit ich nicht wieder daneben liege!",
        },
        "observation": {"en": "Use with lightness; adjust to campaign context.", "es": "Usar con liviandad; ajustar al contexto de la campaña.", "de": "Mit Leichtigkeit verwenden; an Kampagnen-Kontext anpassen."},
    },
    "A30": {
        "trigger": {"en": "Aby greeting (production version, observed in 02/jun test)", "es": "Saludo Aby (versión en producción, observada en test 02/jun)", "de": "Aby-Begrüßung (Produktions-Version, beobachtet im Test 02/jun)"},
        "text": {
            "en": "Hi there! How are you? I'm Aby, virtual assistant of ABSOLUT Sport, official agency of {parceiro} and accredited with {clube_credenciado}. I'm here to help you secure your spot at the best events and games in the world. How would you like to proceed?",
            "es": "¡Hola! ¿Todo bien? Soy Aby, asistente virtual de ABSOLUT Sport, agencia oficial de {parceiro} y acreditada al {clube_credenciado}. Vine a ayudarte a garantizar tu lugar en los mejores eventos y partidos del mundo. ¿Cómo te gustaría seguir?",
            "de": "Hallo! Wie geht's? Ich bin Aby, virtuelle Assistentin von ABSOLUT Sport, offizieller Agentur von {parceiro} und akkreditiert bei {clube_credenciado}. Ich helfe dir, deinen Platz bei den besten Events und Spielen der Welt zu sichern. Wie möchtest du weitermachen?",
        },
        "observation": {"en": "Current production version. Replace A01 when consolidated.", "es": "Versión actual en producción. Sustituir A01 cuando se consolide.", "de": "Aktuelle Produktions-Version. A01 ersetzen, sobald konsolidiert."},
    },
    "A31": {
        "trigger": {"en": "Welcome text when choosing 'Flamengo Games'", "es": "Texto de bienvenida al elegir 'Partidos Flamengo'", "de": "Begrüßungstext bei Wahl von 'Flamengo-Spiele'"},
        "text": {
            "en": "The {estadio} awaits you to experience the {torcida} atmosphere with an official, accredited ticket — all comfort and security so you can enjoy the moment!",
            "es": "El {estadio} te espera para vivir el clima de la {torcida} con entrada oficial y acreditada, con todo confort y seguridad para que disfrutes del momento!",
            "de": "Das {estadio} erwartet dich, um die Atmosphäre der {torcida} mit einem offiziellen, akkreditierten Ticket zu erleben — mit allem Komfort und Sicherheit, damit du den Moment genießen kannst!",
        },
        "observation": {"en": "Captured in 02/jun test. Flamengo at Maracanã example: {estadio}=Maracanã, {torcida}=Nação.", "es": "Capturado en test 02/jun. Ejemplo Flamengo en Maracaná: {estadio}=Maracaná, {torcida}=Nação.", "de": "Im Test 02/jun erfasst. Beispiel Flamengo im Maracanã: {estadio}=Maracanã, {torcida}=Nação."},
    },
    "A32": {
        "trigger": {"en": "Disclaimer 'What you need to know' (CPF + biometrics)", "es": "Disclaimer 'Lo que necesita saber' (CPF + biometría)", "de": "Disclaimer 'Was du wissen musst' (CPF + Biometrie)"},
        "text": {
            "en": "{time_casa} x {time_visitante} | {estadio} ⚠️ Important Information: CPF Notice: The {clube} system accepts only 1 ticket per CPF. If any CPF already has a ticket secured elsewhere, the club system does not allow the redemption of this new ticket. Facial Biometrics: Access to {estadio} is done exclusively via facial biometrics. Make sure each person's registration is updated on the website: {url_biometria}",
            "es": "{time_casa} x {time_visitante} | {estadio} ⚠️ Información Importante: Aviso sobre CPF: El sistema del {clube} acepta sólo 1 entrada por CPF. Si algún CPF ya tiene una entrada garantizada por otro lado, el sistema del club no permite el rescate de esa nueva entrada. Biometría Facial: El acceso al {estadio} se hace exclusivamente vía biometría facial. Asegurate de que el registro de cada persona esté actualizado en el sitio: {url_biometria}",
            "de": "{time_casa} x {time_visitante} | {estadio} ⚠️ Wichtige Informationen: CPF-Hinweis: Das System von {clube} akzeptiert nur 1 Ticket pro CPF. Hat ein CPF bereits ein Ticket anderswo gesichert, lässt das Club-System den Bezug dieses neuen Tickets nicht zu. Gesichts-Biometrie: Der Zugang zum {estadio} erfolgt ausschließlich per Gesichts-Biometrie. Stelle sicher, dass die Registrierung jeder Person auf der Website aktualisiert ist: {url_biometria}",
        },
        "observation": {"en": "Item 39 of the Comparative. Anticipate in a dedicated node between 'Flamengo Games' and match selection. Flamengo biometrics URL: https://biometria.flamengo.com.br/", "es": "Ítem 39 del Comparativo. Anticipar en un nodo dedicado entre 'Partidos Flamengo' y la selección del partido. URL biometría Flamengo: https://biometria.flamengo.com.br/", "de": "Punkt 39 des Vergleichs. In dediziertem Node zwischen 'Flamengo-Spiele' und Match-Auswahl vorwegnehmen. URL Flamengo-Biometrie: https://biometria.flamengo.com.br/"},
    },
    "A33": {
        "trigger": {"en": "'Maracanã Mais' package template", "es": "Plantilla Paquete 'Maracanã Mais'", "de": "Vorlage Paket 'Maracanã Mais'"},
        "text": {
            "en": "'Maracanã Mais' Package — Your spot secured with assigned seat, food and drink included without queues, with full security to the gate and exclusive parking inside the {estadio}! The Ticket: Official ticket for the Maracanã Mais Sector (numbered seat). Food and Drink: Full buffet included with non-alcoholic drinks released (beer available for purchase in the sector). Transport: Accredited transfer with drop-off and parking at {ponto_desembarque} (inside the stadium complex). ⚠️ Important: The transfer departs from a pre-defined meeting point, communicated up to {antecedencia_aviso} before the game. Price: {valor} per person",
            "es": "Paquete 'Maracanã Mais' — Tu lugar garantizado con asiento marcado, comida y bebida incluidas sin fila, con toda seguridad hasta el portón y con estacionamiento exclusivo dentro del {estadio}! La Entrada: Entrada oficial para el Sector Maracanã Mais (asiento numerado). Comida y Bebida: Buffet completo incluido con bebidas no alcohólicas liberadas (cerveza disponible para compra en el sector). Transporte: Transfer acreditado con desembarque y estacionamiento en {ponto_desembarque} (dentro del complejo del estadio). ⚠️ Importante: La salida del transfer ocurre desde un punto de encuentro predefinido, comunicado hasta {antecedencia_aviso} antes del partido. Valor: {valor} por persona",
            "de": "'Maracanã Mais'-Paket — Dein gesicherter Platz mit reserviertem Sitz, Essen und Trinken inklusive ohne Schlange, mit voller Sicherheit bis zum Eingang und exklusivem Parkplatz innerhalb des {estadio}! Das Ticket: Offizielles Ticket für den Sektor Maracanã Mais (nummerierter Sitz). Essen und Trinken: Vollständiges Buffet inklusive nicht-alkoholischer Getränke (Bier im Sektor käuflich erhältlich). Transport: Akkreditierter Transfer mit Ausstieg und Parken am {ponto_desembarque} (innerhalb des Stadion-Komplexes). ⚠️ Wichtig: Die Abfahrt des Transfers erfolgt von einem vordefinierten Treffpunkt, mitgeteilt bis zu {antecedencia_aviso} vor dem Spiel. Preis: {valor} pro Person",
        },
        "observation": {"en": "Captured in 02/jun test. Use as template for other packages (Espaço Fla+, Oeste Inferior, hospitality).", "es": "Capturado en test 02/jun. Usar como plantilla para otros paquetes (Espaço Fla+, Oeste Inferior, hospitality).", "de": "Im Test 02/jun erfasst. Als Vorlage für andere Pakete verwenden (Espaço Fla+, Oeste Inferior, Hospitality)."},
    },
    "A34": {
        "trigger": {"en": "'Buy now' streamlined (item 41 of the Comparative)", "es": "'Comprar ahora' enxuto (ítem 41 del Comparativo)", "de": "'Jetzt kaufen' verschlankt (Punkt 41 des Vergleichs)"},
        "text": {
            "en": "The {estadio} awaits you! ❤️🤍 The best sectors sell out first. Secure yours now. 🔗 Click the link to secure your spot: {url}",
            "es": "¡El {estadio} te espera! ❤️🤍 Los mejores sectores se agotan primero. Asegurá el tuyo ahora. 🔗 Hacé click en el link para garantizar tu lugar: {url}",
            "de": "Das {estadio} erwartet dich! ❤️🤍 Die besten Sektoren sind zuerst ausverkauft. Sichere dir deinen jetzt. 🔗 Klicke auf den Link, um deinen Platz zu sichern: {url}",
        },
        "observation": {"en": "Version proposed in item 41 (streamlining). Game data already appears on the card (item 40), don't repeat here.", "es": "Versión propuesta en el ítem 41 (enxutamiento). Los datos del partido ya aparecen en la tarjeta (ítem 40), no repetir aquí.", "de": "Vorgeschlagene Version in Punkt 41 (Verschlankung). Spieldaten erscheinen bereits auf der Karte (Punkt 40), hier nicht wiederholen."},
    },
    "A35": {
        "trigger": {"en": "'It worked' confirmation (captured from bot in production)", "es": "Confirmación 'Salió bien' (capturada del bot en producción)", "de": "'Hat geklappt'-Bestätigung (vom Bot in Produktion erfasst)"},
        "text": {
            "en": "Great! In the coming days you will receive all the detailed information about your package, ticket, transfer and game day! ⚠️ Don't forget the facial biometrics registration: 🔗 {url_biometria} See you soon! {cores_emojis_clube}",
            "es": "¡Qué bueno! En los próximos días vas a recibir toda la información detallada sobre tu paquete, entrada, transfer y sobre el día del partido! ⚠️ No te olvides del registro de la biometría facial: 🔗 {url_biometria} ¡Hasta pronto! {cores_emojis_clube}",
            "de": "Super! In den kommenden Tagen erhältst du alle detaillierten Informationen zu deinem Paket, Ticket, Transfer und zum Spieltag! ⚠️ Vergiss nicht die Gesichts-Biometrie-Registrierung: 🔗 {url_biometria} Bis bald! {cores_emojis_clube}",
        },
        "observation": {"en": "Captured in 02/jun test. For Flamengo: {cores_emojis_clube}='red/black'.", "es": "Capturado en test 02/jun. Para Flamengo: {cores_emojis_clube}='rojo/negro'.", "de": "Im Test 02/jun erfasst. Für Flamengo: {cores_emojis_clube}='rot/schwarz'."},
    },
}


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
            "gov.contract.title":     "Contractual text",
            "gov.contract.body":      "Message A20 (Cancellation policy) is contractual text. Do not alter without legal review.",
            "gov.inventory.title":    "Inventory",
            "gov.inventory.body":     "Inventory messages (flights, hotel, private boxes) assume \"sold out\". Review at each event according to actual stock.",
            "gov.aby.title":          "Link with Aby",
            "gov.aby.body":           "A24, A25, A26 and A28 correspond to items 01/03, 31, 04 and 32 of the bot audit. This copy is the canonical source.",
            "gov.reuse.title":        "Reuse per event",
            "gov.reuse.body":         "For a new event, just rewrite the variable dictionary. The copy serves any event.",
            "gov.placeholders.title": "⚠️ Localized placeholders",
            "gov.placeholders.body":  "Placeholders ({name}, {nombre}, {berater}) are localized for human readability. The ManyChat/Aby in production only understands the PT version ({nome}, {atendente}). If feeding the bot, copy the PT version. If using manually, replace placeholders with real values before sending.",
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
            "gov.contract.title":     "Texto contractual",
            "gov.contract.body":      "El mensaje A20 (Política de cancelación) es texto contractual. No alterar sin revisión jurídica.",
            "gov.inventory.title":    "Inventario",
            "gov.inventory.body":     "Los mensajes de inventario (vuelos, hotel, palco) asumen \"agotado\". Revisar en cada evento según stock real.",
            "gov.aby.title":          "Vínculo con Aby",
            "gov.aby.body":           "A24, A25, A26 y A28 corresponden a los ítems 01/03, 31, 04 y 32 de la auditoría del bot. Esta copy es la fuente canónica.",
            "gov.reuse.title":        "Reuso por evento",
            "gov.reuse.body":         "Para un nuevo evento, basta con reescribir el diccionario de variables. La copy sirve para cualquier evento.",
            "gov.placeholders.title": "⚠️ Placeholders localizados",
            "gov.placeholders.body":  "Los placeholders ({name}, {nombre}, {berater}) están localizados para lectura humana. El ManyChat/Aby en producción sólo entiende la versión PT ({nome}, {atendente}). Si vas a alimentar el bot, copiá la versión PT. Si vas a usar manualmente, sustituí los placeholders por los valores reales antes de enviar.",
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
            "gov.contract.title":     "Vertragstext",
            "gov.contract.body":      "Nachricht A20 (Stornierungsrichtlinie) ist Vertragstext. Nicht ohne juristische Prüfung ändern.",
            "gov.inventory.title":    "Bestand",
            "gov.inventory.body":     "Bestands-Nachrichten (Flüge, Hotel, Logen) gehen von „ausverkauft“ aus. Bei jedem Event nach tatsächlichem Bestand prüfen.",
            "gov.aby.title":          "Verbindung mit Aby",
            "gov.aby.body":           "A24, A25, A26 und A28 entsprechen den Punkten 01/03, 31, 04 und 32 des Bot-Audits. Diese Copy ist die kanonische Quelle.",
            "gov.reuse.title":        "Wiederverwendung pro Event",
            "gov.reuse.body":         "Für ein neues Event reicht es, das Variablen-Wörterbuch neu zu schreiben. Die Copy dient für jedes Event.",
            "gov.placeholders.title": "⚠️ Lokalisierte Platzhalter",
            "gov.placeholders.body":  "Die Platzhalter ({name}, {nombre}, {berater}) sind für menschliche Lesbarkeit lokalisiert. Das ManyChat/Aby in Produktion versteht nur die PT-Version ({nome}, {atendente}). Wenn der Bot gefüttert wird, kopiere die PT-Version. Bei manueller Verwendung ersetze die Platzhalter vor dem Senden durch die echten Werte.",
        },
    }
    out = dict(base_ui[lang])
    # Categorias: traduzir via CAT_TRANSLATIONS
    # Variáveis: traduzir via VAR_TRANSLATIONS (meaning + example)
    # Mensagens: traduzir via MSG_TRANSLATIONS (text + trigger + observation)
    # Fallback para PT se a tradução não existir no mapa (não deve ocorrer
    # se os 3 mapas estão completos).
    for key in pt:
        if key.startswith("lib.cat."):
            pt_name = pt[key]
            translated = CAT_TRANSLATIONS.get(pt_name, {}).get(lang)
            out[key] = translated if translated else pt_name
        elif key.startswith("lib.var."):
            # chave: lib.var.{name}.{meaning|example}
            parts = key.split(".")
            if len(parts) >= 4:
                var_name, field = parts[2], parts[3]
                tr = VAR_TRANSLATIONS.get(var_name, {}).get(field, {}).get(lang)
                out[key] = tr if tr else pt[key]
            else:
                out[key] = pt[key]
        elif key.startswith("lib.msg."):
            # chave: lib.msg.{ID}.{text|trigger|observation}
            parts = key.split(".")
            if len(parts) >= 4:
                msg_id, field = parts[2], parts[3]
                tr = MSG_TRANSLATIONS.get(msg_id, {}).get(field, {}).get(lang)
                if tr is not None:
                    # Localiza placeholders {nome}→{name} (etc.) só em campos
                    # que podem conter variáveis (text + observation).
                    # trigger não tem placeholders.
                    if field in ("text", "observation"):
                        tr = localize_placeholders(tr, lang)
                    out[key] = tr
                else:
                    out[key] = f"[TODO {lang.upper()}] {pt[key]}"
            else:
                out[key] = pt[key]
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
        # Mapa de placeholders localizados: o front usa para renderizar
        # chips de variáveis e a tabela do dicionário no idioma ativo.
        # Aviso: ManyChat/Aby em produção espera nomes PT — versões
        # localizadas servem para leitura humana.
        "placeholders": PLACEHOLDER_TRANSLATIONS,
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
