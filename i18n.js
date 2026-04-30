/**
 * ABSOLUT Sport — Design System i18n
 * Shared language toggle for PT · EN · ES.
 * Each page sets `window.I18N_DICT = { pt: {...}, en: {...}, es: {...} }` before loading this script.
 * Translatable elements use `data-i18n="key"` (textContent) or `data-i18n-html="key"` (innerHTML).
 */
(function () {
  const STORAGE_KEY = 'asb_lang';
  const DEFAULT_LANG = 'pt';
  const LANGS = ['pt', 'en', 'es', 'de'];

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
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : lang === 'de' ? 'de-DE' : lang;

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const v = dict[el.dataset.i18n];
      if (v !== undefined) el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const v = dict[el.dataset.i18nHtml];
      if (v !== undefined) el.innerHTML = v;
    });
    document.querySelectorAll('[data-i18n-attr]').forEach(el => {
      // format: "attr:key" — multiple separated by ;
      el.dataset.i18nAttr.split(';').forEach(pair => {
        const [attr, key] = pair.split(':');
        if (attr && key && dict[key.trim()] !== undefined) {
          el.setAttribute(attr.trim(), dict[key.trim()]);
        }
      });
    });

    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // Re-run zero-to-O for any SoulCraft text that just changed
    requestAnimationFrame(replaceZerosInSoulCraft);
  }

  function replaceZerosInSoulCraft() {
    document.querySelectorAll('*').forEach(el => {
      const font = (getComputedStyle(el).fontFamily || '').toLowerCase();
      if (!font.includes('soulcraft')) return;
      el.childNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE && node.textContent.includes('0')) {
          node.textContent = node.textContent.replaceAll('0', 'O');
        }
      });
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
