import { INTL_LOCALE, type Lang } from '@/i18n';

export function formatDate(date: Date, lang: Lang, style: 'long' | 'month' | 'year' = 'long'): string {
  const options: Intl.DateTimeFormatOptions =
    style === 'long'
      ? { day: 'numeric', month: 'long', year: 'numeric' }
      : style === 'month'
        ? { month: 'short', year: 'numeric' }
        : { year: 'numeric' };
  return new Intl.DateTimeFormat(INTL_LOCALE[lang], { ...options, timeZone: 'UTC' }).format(date);
}

/** "2022-03" -> Date (UTC, first of month). */
export function parseYearMonth(value: string): Date {
  const [y, m] = value.split('-').map(Number);
  return new Date(Date.UTC(y!, (m ?? 1) - 1, 1));
}

export function isoDate(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function pad2(n: number): string {
  return String(n).padStart(2, '0');
}
