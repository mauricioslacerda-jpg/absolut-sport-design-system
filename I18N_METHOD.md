# Método i18n — Replicável

Como traduzimos páginas estáticas pra múltiplos idiomas no ABSOLUT Sport Design System, e como aplicar a mesma dinâmica em qualquer projeto HTML.

> **TL;DR:** Um script JS de ~70 linhas + um dicionário inline em cada página + atributos `data-i18n` no HTML. Sem build, sem framework, sem dependência externa. Funciona em `file://`, GitHub Pages, S3, qualquer host estático.

---

## Quando usar

✅ Sites estáticos (HTML/CSS/JS puro)
✅ Páginas de marketing, design systems, playbooks, landing pages
✅ Projetos pequenos a médios (até ~30 páginas)
✅ Você controla o HTML e quer ler o conteúdo PT direto no source
✅ Acesso público sem login

## Quando não usar

❌ App SPA com React/Vue/Svelte — usa o i18n nativo do framework (react-intl, vue-i18n, etc.)
❌ Mais de 50 páginas — vale extrair pra arquivos JSON externos
❌ Conteúdo dinâmico vindo de CMS — i18n é responsabilidade do backend
❌ Mais de 8 idiomas — começa a virar guerra de manutenção inline

---

## Arquitetura

```
projeto/
├── i18n.js                  ← lógica do toggle (copia esse arquivo)
├── index.html               ← conteúdo PT inline + window.I18N_DICT por idioma
├── pagina-2.html            ← outro dicionário inline (cada página é autônoma)
└── ...
```

**Princípios de design:**
1. **PT inline no HTML** — funciona sem JS, fallback grátis se carregar quebrar
2. **Dicionário por página** — cada HTML carrega só o que precisa, autonomia total
3. **Toggle persistente em localStorage** — preferência sobrevive entre páginas e visitas
4. **Zero dependências** — copia 2 arquivos e roda

---

## O `i18n.js` completo

Cole esse arquivo na raiz do projeto. ~70 linhas, sem dependências.

```js
/**
 * i18n.js — toggle de idioma para sites estáticos
 *
 * Cada HTML define `window.I18N_DICT = { pt: {...}, en: {...} }` antes
 * de carregar este script. Elementos traduzíveis usam:
 *   - data-i18n="chave"           (textContent)
 *   - data-i18n-html="chave"      (innerHTML, preserva markup)
 *   - data-i18n-attr="title:chave" (atributos HTML)
 *
 * Toggle UI: botões com classe .lang-btn e data-lang="pt|en|...".
 */
(function () {
  const STORAGE_KEY = 'site_lang';        // troque por nome único do projeto
  const DEFAULT_LANG = 'pt';
  const LANGS = ['pt', 'en', 'es', 'de']; // ajuste conforme idiomas suportados

  function getLang() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return (stored && LANGS.includes(stored)) ? stored : DEFAULT_LANG;
  }

  function setLang(lang) {
    if (!LANGS.includes(lang)) lang = DEFAULT_LANG;
    localStorage.setItem(STORAGE_KEY, lang);
    apply(lang);
  }

  function apply(lang) {
    const dict = (window.I18N_DICT && window.I18N_DICT[lang]) || {};

    // Atualiza o atributo <html lang> dinamicamente (a11y + SEO)
    document.documentElement.lang =
      lang === 'pt' ? 'pt-BR' :
      lang === 'de' ? 'de-DE' :
      lang;

    // Texto puro
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const v = dict[el.dataset.i18n];
      if (v !== undefined) el.textContent = v;
    });

    // Texto com markup
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const v = dict[el.dataset.i18nHtml];
      if (v !== undefined) el.innerHTML = v;
    });

    // Atributos (title, aria-label, placeholder, alt...)
    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
      el.dataset.i18nAttr.split(';').forEach(pair => {
        const [attr, key] = pair.split(':');
        if (attr && key && dict[key.trim()] !== undefined) {
          el.setAttribute(attr.trim(), dict[key.trim()]);
        }
      });
    });

    // Marca botão ativo do toggle
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
  }

  function init() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => setLang(btn.dataset.lang));
    });
    apply(getLang());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

**Customizar pra cada projeto:**

| Variável | Padrão | Trocar quando |
|---|---|---|
| `STORAGE_KEY` | `'site_lang'` | Sempre — use nome único do projeto pra não colidir com outros sites no mesmo domínio |
| `DEFAULT_LANG` | `'pt'` | Se o canônico for outro idioma |
| `LANGS` | `['pt','en','es','de']` | Adicionar/remover conforme escopo |

---

## Os 3 atributos do HTML

### 1. `data-i18n` — texto puro

Use quando não tem markup interno.

```html
<h1 data-i18n="hero.title">Título canônico em português</h1>
<p data-i18n="hero.sub">Parágrafo de apoio.</p>
<button data-i18n="cta.save">Salvar</button>
```

### 2. `data-i18n-html` — texto com markup

Use quando tem `<br>`, `<strong>`, `<span class="accent">`, `<code>`, `<a>`.

```html
<h2 data-i18n-html="section.title">
  Linha 1<br><span class="accent">Linha 2.</span>
</h2>

<p data-i18n-html="legal.terms">
  Ao continuar, você concorda com os <a href="/termos">termos</a>.
</p>
```

### 3. `data-i18n-attr="atributo:chave"` — atributos HTML

Use pra `title`, `aria-label`, `placeholder`, `alt`. Múltiplos atributos no mesmo elemento separam por `;`.

```html
<a data-i18n-attr="title:nav.credit.title"
   title="Padrão em português">
  MM × RR
</a>

<input data-i18n-attr="placeholder:form.email.ph;aria-label:form.email.aria"
       placeholder="seu@email.com">

<img data-i18n-attr="alt:hero.alt" src="hero.jpg" alt="Estádio à noite">
```

---

## O dicionário inline

No final do `<body>`, **antes** do `<script src="i18n.js">`:

```html
<script>
window.I18N_DICT = {
  pt: {
    'hero.title':'Título em português',
    'hero.sub':'Parágrafo de apoio.',
    'section.title':'Linha 1<br><span class="accent">Linha 2.</span>',
    'cta.save':'Salvar',
    'nav.credit.title':'Sugestões pra design@',
    'form.email.ph':'seu@email.com',
    'form.email.aria':'Campo de e-mail',
    'hero.alt':'Estádio à noite',
    'legal.terms':'Ao continuar, você concorda com os <a href="/termos">termos</a>.'
  },
  en: {
    'hero.title':'Title in English',
    'hero.sub':'Supporting paragraph.',
    'section.title':'Line 1<br><span class="accent">Line 2.</span>',
    'cta.save':'Save',
    'nav.credit.title':'Suggestions to design@',
    'form.email.ph':'you@email.com',
    'form.email.aria':'Email field',
    'hero.alt':'Stadium at night',
    'legal.terms':'By continuing, you agree to the <a href="/terms">terms</a>.'
  },
  es: { /* ... */ },
  de: { /* ... */ }
};
</script>

<script src="i18n.js"></script>
```

**Por que inline e não JSON externo:**
- Zero requisição HTTP extra
- Funciona em `file://` (sem servidor)
- Cada página é autônoma — quebrar uma não afeta as outras
- Diff do git mostra tradução nova junto com a feature

---

## Convenção de nomes de chave

Padrão: `secao.subsecao.campo`

```js
'hero.title'           // bloco hero, título
'hero.sub'             // bloco hero, sub
'pil.p1.name'          // pilar 1, nome
'pil.p1.def'           // pilar 1, definição
'pil.p1.metric'        // pilar 1, métrica
'met.cac.n'            // métrica CAC, nome (n)
'met.cac.w'            // métrica CAC, why (w)
'met.cac.b'            // métrica CAC, benchmark (b)
'footer.col1'          // footer, coluna 1
'nav.logos'            // nav, link logos
```

**Vantagens:**
- Agrupa visualmente no dicionário (todas as `pil.*` ficam juntas)
- Procura rápida (`Ctrl+F` por `met.` lista todas as métricas)
- Facilita renomes (refatora o prefixo inteiro de uma vez)

**Anti-padrão:**
- `meu_titulo_principal` (snake_case longo, vira ruído)
- `t1`, `t2`, `t3` (inscrutável fora de contexto)
- Chave em PT (`titulo`, `descricao`) — funciona, mas mistura idiomas no código

---

## O HTML do toggle

### Markup

```html
<div class="lang-toggle" role="group" aria-label="Language">
  <button class="lang-btn" data-lang="pt" aria-label="Português">PT</button>
  <button class="lang-btn" data-lang="en" aria-label="English">EN</button>
  <button class="lang-btn" data-lang="es" aria-label="Español">ES</button>
  <button class="lang-btn" data-lang="de" aria-label="Deutsch">DE</button>
</div>
```

### CSS de referência (pill segmentado)

```css
.lang-toggle {
  display: inline-flex;
  background: #141414;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 100px;
  padding: 3px;
  gap: 2px;
}
.lang-btn {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  padding: 5px 10px;
  border-radius: 100px;
  background: transparent;
  color: #9A9A9A;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease-out;
}
.lang-btn:hover { color: #fff; }
.lang-btn.active {
  background: #155F97;  /* cor de marca do projeto */
  color: #fff;
}
```

A classe `.active` aparece automática no botão certo — o `i18n.js` cuida disso.

---

## Voz e processo de tradução

### Ordem que funciona

1. **Escreve PT primeiro** com tudo inline no HTML. Voz, ritmo, referências culturais nascem aqui.
2. **Constrói a página completa em PT.** Vê layout, ajusta CSS, valida UX.
3. **Só depois traduz** os outros idiomas. Cria `en`, `es`, `de` no dicionário lendo PT como referência.
4. **Adapta, não traduz literal.**

### Aforismos preservam ritmo, não palavra

| PT | EN |
|---|---|
| "Lista de ideias não é plano." | "A list of ideas is not a plan." |
| "Quem não mede, supõe." | "If you don't measure, you guess." |
| "Sobe quem tem o lápis na mão." | "Whoever holds the pen, uploads." |

A frase em EN não é tradução automática. É a versão **que tem o mesmo peso** no idioma.

### Termos preservados em todos os idiomas

- Nomes de marca: produtos, empresas, ferramentas
- Termos técnicos universais: Hero, Display, Headline, Tokens, Workflow, ICE, AAARRR, KPI, ROAS
- Marcas registradas com símbolo: `Libertadores™`, `iPhone®`
- Nomes próprios: pessoas, lugares, eventos

### Adaptações regionais

- **Espanhol:** voseo onde fizer sentido (Buenos Aires, Argentina). `Sabés vender el mejor lugar` em vez de `Sabes vender`.
- **Alemão:** registro `du` (informal) por padrão. `Sie` (formal) só se o público for institucional formal.
- **Inglês:** decidir entre US e UK. Inglês neutro internacional funciona pra maioria dos contextos B2B.
- **Português:** PT-BR vs PT-PT. Decidir cedo e seguir.

---

## Passo a passo — criar uma nova página traduzida

1. Crie o arquivo `nova-pagina.html` com a estrutura HTML padrão
2. Escreva o conteúdo todo em PT, marcando elementos traduzíveis com `data-i18n="chave"` e texto inline
3. No final do `<body>`, adicione:
   ```html
   <script>
   window.I18N_DICT = {
     pt: {
       'chave1':'Texto em PT 1',
       'chave2':'Texto em PT 2'
     }
   };
   </script>
   <script src="i18n.js"></script>
   ```
4. Adicione o markup do toggle no header
5. Abra no navegador. PT funciona, toggle ainda só tem 1 idioma — esperado.
6. Adicione bloco `en: { ... }` no dicionário, traduzindo cada chave
7. Recarrega, clica EN no toggle. Tudo deve trocar.
8. Repete pra `es`, `de`, etc.
9. Commita.

---

## Checklist antes de publicar

- [ ] Todas as chaves usadas no HTML têm correspondente em **todos** os idiomas
- [ ] Texto inline default (PT) é igual ao valor de `pt` no dicionário
- [ ] Toggle aparece e os botões têm `data-lang` correto
- [ ] `<html lang>` muda dinamicamente no inspector quando troca idioma
- [ ] localStorage persiste a escolha (refresh mantém o idioma)
- [ ] Mobile: toggle acessível ou esconde com fallback aceitável
- [ ] Termos de marca preservados em todos os idiomas
- [ ] Aforismos têm versão equivalente, não literal
- [ ] `data-i18n-html` em qualquer chave que tenha `<br>`, `<strong>`, `<span>`, `<a>` ou `<code>`
- [ ] OG tags traduzidas se quiser previews multilíngues no LinkedIn/WhatsApp

---

## Gotchas (aprendidos no caminho)

### 1. `<br>` quebra com `data-i18n` simples
Se a chave tem `<br>`, **tem que ser** `data-i18n-html`. Senão o `<br>` aparece como texto literal "<br>".

### 2. Aspas escapadas em chaves com `'`
Texto com apóstrofo (`don't`, `c'est`) precisa escape no JS:
```js
'guide.dont':'Don\'t'   // ✓
"guide.dont":"Don't"    // ✓ (aspas duplas no wrap)
```

### 3. `replace_all` em chaves duplicadas
Se 2 idiomas têm a mesma string PT temporariamente, `Edit replace_all` troca os dois. Edita um por um nesse caso.

### 4. localStorage em `file://`
Funciona, mas tem quirks. Em produção HTTPS, sem problema.

### 5. Re-renderizar elementos dinâmicos
Se você criar elementos via JS DEPOIS do `init()` do i18n, eles não vão ter as chaves aplicadas. Soluções:
- Aplicar manualmente: `apply(getLang())` depois de criar o elemento
- Usar `MutationObserver` (mais complexo, raramente vale)
- Renderizar com texto traduzido direto via `window.I18N_DICT[lang][key]`

### 6. SoulCraft (ou outras fontes variáveis) + i18n
Se trocar texto via `textContent`, a fonte re-renderiza. Sem problema. Mas se você tem scripts como `zero-to-o.js` que processam DOM, lembre de re-rodá-los após `apply()` ou use `MutationObserver`.

### 7. Mensagens de erro do navegador
Browsers mostram mensagens nativas (form validation, alerts) no idioma do navegador, não no idioma do toggle. Pra controlar, use validação JS customizada.

---

## Trade-offs e quando expandir

### Esse método é bom até ~30 páginas e ~6 idiomas

Acima disso, considere:

| Sintoma | Próximo passo |
|---|---|
| Strings duplicadas em muitas páginas | Extrair pra arquivos `locales/pt.json`, `locales/en.json` carregados via `fetch` |
| Build pipeline existente | Migrar pra `i18next`, `lingui`, `react-intl`, ou framework nativo |
| Tradução por agência externa | Adotar formato XLIFF ou Crowdin/Lokalise pra fluxo profissional |
| Conteúdo vindo de CMS | i18n vira responsabilidade do backend (Strapi, Contentful, etc.) |
| Mais de 6 idiomas | Pesar custo de manutenção vs valor real por idioma |

### Quando esse método é insubstituível

- Sites estáticos pequenos sem build
- Demos, prototipos, landing pages
- Documentação técnica (design systems, playbooks, manuais)
- Páginas internas/B2B com público multilíngue conhecido
- Quando você quer que o source HTML seja legível pelo time de conteúdo

---

## Exemplo vivo

Este método tá rodando em produção em:

- `https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/` (Hub, 4 idiomas)
- `https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/playbooks/ai-marketing.html` (4 idiomas)
- `https://mauricioslacerda-jpg.github.io/absolut-sport-design-system/playbooks/growth.html` (4 idiomas)

3 páginas, 4 idiomas (PT/EN/ES/DE), ~1000 strings totais. Zero build, zero framework, hospedado em GitHub Pages grátis.

---

## Replicação rápida — kit mínimo

Pra começar agora num projeto novo:

1. **Copie 1 arquivo** pro novo projeto: `i18n.js` (~70 linhas, está acima neste documento).
2. **Edite 3 valores** no topo: `STORAGE_KEY`, `DEFAULT_LANG`, `LANGS`.
3. **Em cada HTML novo**:
   - Adicione `data-i18n` aos elementos traduzíveis
   - Adicione o `<div class="lang-toggle">` no header
   - Adicione o `<script>window.I18N_DICT = {...}</script>` antes do `<script src="i18n.js">`
4. **Escreva PT primeiro.** Traduza depois.

Pronto. Sem `npm install`, sem build, sem deploy diferente.

---

## Manutenção

### Adicionando um novo idioma

1. Adicione o código ISO no array `LANGS` do `i18n.js` (ex: `'fr'`)
2. Adicione um botão no toggle: `<button class="lang-btn" data-lang="fr">FR</button>`
3. Em cada HTML, adicione o bloco `fr: { ... }` no `window.I18N_DICT`
4. Traduza todas as chaves

### Adicionando um novo texto traduzível

1. Marque o elemento no HTML com `data-i18n="nova.chave"`
2. Adicione `'nova.chave':'Texto'` em **todos** os idiomas no dicionário (não esquece nenhum)
3. Salva. Funciona.

### Renomeando uma chave

`Find & Replace` em todo o arquivo (HTML + dicionários). Se a chave aparece em vários HTMLs, repete em cada um. Use prefixo único (`prj.`) pra evitar colisões em find/replace.

---

## Licença e atribuição

Este método nasceu no ABSOLUT Sport Design System. Use livremente em qualquer projeto. Se replicar e melhorar, manda PR ou um e-mail pra `design@absolut-sport.com.br` — sempre bom saber onde o método tá rodando.

—
**Mauricio Lacerda × Rafa Rafa**
ABSOLUT Sport Design System
2026
