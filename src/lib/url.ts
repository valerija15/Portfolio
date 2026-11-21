/**
 * Base-path aware URLs. The site can be served from a domain root ("/") or a
 * sub-path such as GitHub Pages' "/Portfolio/" (set BASE_PATH at build time).
 */
export const BASE = import.meta.env.BASE_URL.replace(/\/+$/, '');

/** Prefix a root-relative path ("/lv/") with the base path. External URLs pass through. */
export function withBase(path: string): string {
  if (!path.startsWith('/') || path.startsWith('//')) return path;
  return BASE + path;
}

/** Remove the base path from a pathname (inverse of withBase). */
export function stripBase(pathname: string): string {
  return BASE && pathname.startsWith(BASE) ? pathname.slice(BASE.length) || '/' : pathname;
}
