// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Public URL of the deployed site — used for canonical URLs, hreflang,
// Open Graph and the sitemap. Override with SITE_URL at build time.
const SITE_URL = process.env.SITE_URL ?? 'https://anna-berzina.example.com';
// Sub-path the site is served from. "/" for a domain root (Netlify, Vercel, custom domain);
// "/Portfolio" for GitHub Pages at https://<user>.github.io/Portfolio/.
const BASE_PATH = process.env.BASE_PATH ?? '/';
const ROOT_URL = new URL(BASE_PATH.replace(/\/?$/, '/'), SITE_URL).href;

export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  image: {
    responsiveStyles: false,
  },
  integrations: [
    sitemap({
      filter: (page) => page !== ROOT_URL && !/\/404\/?$/.test(page),
      i18n: {
        defaultLocale: 'lv',
        locales: { lv: 'lv-LV', en: 'en-GB' },
      },
    }),
  ],
});
