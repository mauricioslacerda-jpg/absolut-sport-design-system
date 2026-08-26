/**
 * ABSOLUT Sport — SoulCraft Zero-to-O
 * Automatically replaces all digit "0" with letter "O" in any element
 * rendered with the SoulCraft font. Run once after DOM is ready.
 * Include in every HTML file that uses SoulCraft.
 */
(function applySoulCraftZeroToO() {
  function isSoulCraft(el) {
    const font = getComputedStyle(el).fontFamily || '';
    return font.toLowerCase().includes('soulcraft');
  }

  function replaceZeros(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (node.textContent.includes('0')) {
        node.textContent = node.textContent.replaceAll('0', 'O');
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      node.childNodes.forEach(replaceZeros);
    }
  }

  function processElement(el) {
    if (isSoulCraft(el)) replaceZeros(el);
  }

  function run() {
    document.querySelectorAll('*').forEach(processElement);
  }

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }

  // Also observe DOM mutations for React-rendered content
  const observer = new MutationObserver((mutations) => {
    mutations.forEach(m => {
      m.addedNodes.forEach(node => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          processElement(node);
          node.querySelectorAll && node.querySelectorAll('*').forEach(processElement);
        }
      });
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();
