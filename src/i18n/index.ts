import lv from './lv.json';
import en from './en.json';

export const LOCALES = ['lv', 'en'] as const;
export type Lang = (typeof LOCALES)[number];
export const DEFAULT_LANG: Lang = 'lv';
export const HTML_LANG: Record<Lang, string> = { lv: 'lv', en: 'en' };
export const INTL_LOCALE: Record<Lang, string> = { lv: 'lv-LV', en: 'en-GB' };

const dictionaries = { lv, en } as const;
export type Dictionary = typeof lv;

export function isLang(value: unknown): value is Lang {
  return typeof value === 'string' && (LOCALES as readonly string[]).includes(value);
}

/** Static paths helper for every `[lang]` route. */
export function langPaths() {
  return LOCALES.map((lang) => ({ params: { lang } }));
}

/** Returns a translator bound to a locale. Keys use dot notation: t('nav.home'). */
export function useTranslations(lang: Lang) {
  const dict = dictionaries[lang] as unknown as Record<string, unknown>;
  return function t(key: string, vars: Record<string, string | number> = {}): string {
    const value = key.split('.').reduce<unknown>((acc, part) => (acc as Record<string, unknown> | undefined)?.[part], dict);
    if (typeof value !== 'string') {
      throw new Error(`[i18n] Missing string "${key}" for locale "${lang}"`);
    }
    return value.replace(/\{(\w+)\}/g, (_, name) => String(vars[name] ?? `{${name}}`));
  };
}

/** Pick a localized value from a `{ lv, en }` object. */
export function l<T>(value: { lv: T; en: T }, lang: Lang): T {
  return value[lang];
}

export const otherLang = (lang: Lang): Lang => (lang === 'lv' ? 'en' : 'lv');
