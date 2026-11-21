// Remember the visitor's language — used ONLY to redirect the bare "/" route.
const KEY = 'preferred-lang';
function save(lang: string | null | undefined) {
  if (lang !== 'lv' && lang !== 'en') return;
  try { localStorage.setItem(KEY, lang); } catch { /* storage unavailable */ }
}
save(document.documentElement.lang);
document.addEventListener('click', (e) => {
  const link = (e.target as Element | null)?.closest<HTMLAnchorElement>('[data-lang-link]');
  if (link) save(link.dataset.langLink);
});
