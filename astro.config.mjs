// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Public URL of the deployed site — used for canonical URLs, hreflang,
// Open Graph and the sitemap. Override with SITE_URL at build time.
const SITE_URL = process.env.SITE_URL ?? 'https://anna-berzina.example.com';

export default defineConfig({
  site: SITE_URL,
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  image: {
    responsiveStyles: false,
  },
  integrations: [
    sitemap({
      filter: (page) => !page.endsWith(SITE_URL + '/') && !/\/404\/?$/.test(page),
      i18n: {
        defaultLocale: 'lv',
        locales: { lv: 'lv-LV', en: 'en-GB' },
      },
    }),
  ],
});
