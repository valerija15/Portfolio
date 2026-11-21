import { marked } from 'marked';

marked.use({ gfm: true, breaks: false });

/** Render trusted, author-controlled markdown from content files to HTML. */
export function md(source: string | undefined): string {
  if (!source) return '';
  return marked.parse(source, { async: false }) as string;
}

/** Inline markdown (no wrapping <p>). */
export function mdInline(source: string): string {
  return marked.parseInline(source, { async: false }) as string;
}
