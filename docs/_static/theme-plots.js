/* Select figure assets matching Furo's explicit theme or the system preference. */
(() => {
  const preference = window.matchMedia('(prefers-color-scheme: dark)');
  function updatePlots() {
    const setting = document.body.dataset.theme;
    const dark = setting === 'dark' || (setting !== 'light' && preference.matches);
    document.querySelectorAll('article img[src*="generated/"]').forEach(img => {
      const current = img.getAttribute('src');
      if (!current.endsWith('.png')) return;
      const light = img.dataset.lightSrc || current.replace(/-dark\.png$/, '.png');
      img.dataset.lightSrc = light;
      const target = dark ? light.replace(/\.png$/, '-dark.png') : light;
      if (current !== target) img.setAttribute('src', target);
    });
  }
  document.addEventListener('DOMContentLoaded', () => {
    updatePlots();
    new MutationObserver(updatePlots).observe(document.body, {attributes: true, attributeFilter: ['data-theme']});
    preference.addEventListener('change', updatePlots);
  });
})();

// The command remains selectable if clipboard access is unavailable.
document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.install-copy');
  if (!button) return;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(document.querySelector('#install-command').textContent);
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy'; }, 1800);
    } catch {
      button.textContent = 'Select text';
    }
  });
});
