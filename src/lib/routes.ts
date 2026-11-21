import type { Lang } from '@/i18n';
import { LOCALES } from '@/i18n';

/** Route keys used by navigation. Slugs are identical across locales. */
export const NAV = ['home', 'about', 'work', 'experience', 'media', 'contact'] as const;
export type RouteKey = (typeof NAV)[number] | 'privacy';

const SEGMENTS: Record<RouteKey, string> = {
  home: '',
  about: 'about',
  work: 'work',
  experience: 'experience',
  media: 'media',
  contact: 'contact',
  privacy: 'privacy',
};

export function routeUrl(lang: Lang, key: RouteKey): string {
  const seg = SEGMENTS[key];
  return seg ? `/${lang}/${seg}/` : `/${lang}/`;
}

export function projectUrl(lang: Lang, slug: string): string {
  return `/${lang}/work/${slug}/`;
}

/** Same page in another locale: swaps the leading /lv/ or /en/ segment. */
export function switchLocalePath(pathname: string, target: Lang): string {
  const parts = pathname.split('/');
  if ((LOCALES as readonly string[]).includes(parts[1] ?? '')) {
    parts[1] = target;
    return parts.join('/');
  }
  return `/${target}/`;
}

/** Whether a nav item is the current section. */
export function isActive(pathname: string, lang: Lang, key: RouteKey): boolean {
  const url = routeUrl(lang, key);
  const path = pathname.endsWith('/') ? pathname : pathname + '/';
  return key === 'home' ? path === url : path.startsWith(url);
}
