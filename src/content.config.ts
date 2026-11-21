/**
 * Typed content model for the whole site.
 * Every piece of copy lives in src/content/** or src/i18n/*.json — components
 * only render what these schemas describe.
 */
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

/** A string provided in every supported locale. */
const localized = z.object({ lv: z.string().min(1), en: z.string().min(1) });
/** Optional localized markdown block. */
const localizedMd = localized.optional();

export const PROJECT_CATEGORIES = [
  'pr-campaign',
  'media-relations',
  'event-communication',
  'brand-communication',
  'social-media',
  'content-creation',
  'public-events',
  'crisis-communication',
] as const;

export const PUBLICATION_TYPES = [
  'article',
  'press-release',
  'interview',
  'media-appearance',
  'campaign-publication',
  'video-interview',
] as const;

const yearMonth = z.string().regex(/^\d{4}-(0[1-9]|1[0-2])$/, 'Use YYYY-MM');

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{yaml,yml}', base: './src/content/projects' }),
  schema: ({ image }) => {
    const embed = z.object({
      provider: z.enum(['youtube', 'vimeo']),
      id: z.string(),
    });
    const cover = z.discriminatedUnion('type', [
      z.object({ type: z.literal('image'), src: image(), alt: localized }),
      z.object({
        type: z.literal('video'),
        /** Path under /public, e.g. /video/clip.mp4 */
        src: z.string().startsWith('/'),
        webm: z.string().startsWith('/').optional(),
        poster: image(),
        alt: localized,
      }),
    ]);
    const galleryItem = z.discriminatedUnion('type', [
      z.object({ type: z.literal('image'), src: image(), alt: localized, caption: localized.optional() }),
      z.object({
        type: z.literal('video'),
        src: z.string().startsWith('/'),
        webm: z.string().startsWith('/').optional(),
        poster: image(),
        alt: localized,
        caption: localized.optional(),
      }),
      z.object({
        type: z.literal('embed'),
        embed,
        poster: image(),
        alt: localized,
        caption: localized.optional(),
      }),
    ]);
    return z.object({
      slug: z.string().regex(/^[a-z0-9-]+$/),
      featured: z.boolean().default(false),
      /** true while the project uses fictional placeholder figures — shows a disclaimer under results. */
      placeholder: z.boolean().default(false),
      order: z.number().int(),
      layout: z.enum(['large', 'tall', 'wide', 'standard']).default('standard'),
      year: z.number().int().min(1990).max(2100),
      category: z.enum(PROJECT_CATEGORIES),
      client: z.string(),
      role: localized,
      title: localized,
      summary: localized,
      cover,
      overview: localizedMd,
      challenge: localizedMd,
      strategy: localizedMd,
      execution: localizedMd,
      results: z.array(z.object({ value: z.string(), label: localized })).optional(),
      gallery: z.array(galleryItem).optional(),
      links: z
        .array(z.object({ title: localized, url: z.url(), outlet: z.string() }))
        .optional(),
    });
  },
});

const publications = defineCollection({
  loader: glob({ pattern: '**/*.{yaml,yml}', base: './src/content/publications' }),
  schema: ({ image }) =>
    z.object({
      type: z.enum(PUBLICATION_TYPES),
      title: localized,
      date: z.coerce.date(),
      url: z.url(),
      /** Language of the original publication (shown as a hint). */
      language: z.enum(['lv', 'en']).default('lv'),
      outlet: z.object({
        name: z.string(),
        /** Optional real logo. If missing, a typographic wordmark is rendered. */
        logo: image().optional(),
        wordmark: z.enum(['serif', 'sans', 'italic', 'mono', 'condensed']).default('serif'),
      }),
      thumbnail: image().optional(),
      video: z.object({ provider: z.enum(['youtube', 'vimeo']), id: z.string() }).optional(),
      /** Show outlet in the home page "as seen in" strip. */
      highlight: z.boolean().default(false),
    }),
});

const experience = defineCollection({
  loader: file('./src/content/experience.yaml'),
  schema: z.object({
    order: z.number().int(),
    organisation: z.string(),
    position: localized,
    location: localized.optional(),
    start: yearMonth,
    /** null / omitted = present */
    end: yearMonth.nullable().optional(),
    description: localized,
    achievements: z.array(localized).optional(),
  }),
});

const education = defineCollection({
  loader: file('./src/content/education.yaml'),
  schema: z.object({
    order: z.number().int(),
    kind: z.enum(['education', 'certification']),
    institution: localized,
    qualification: localized,
    start: yearMonth.optional(),
    end: yearMonth,
    description: localized.optional(),
  }),
});

const testimonials = defineCollection({
  loader: file('./src/content/testimonials.yaml'),
  schema: z.object({
    order: z.number().int(),
    quote: localized,
    name: z.string(),
    role: localized,
    organisation: z.string(),
    /** Placeholder testimonials must stay flagged until replaced with real, approved quotes. */
    fictional: z.boolean().default(false),
  }),
});

const site = defineCollection({
  loader: glob({ pattern: 'site.yaml', base: './src/content/site' }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      title: localized,
      location: localized,
      email: z.email(),
      phone: z.string().optional(),
      showPhone: z.boolean().default(false),
      socials: z.object({ linkedin: z.url() }),
      /** Contact form. Leave endpoint empty to fall back to a prefilled mailto: link. */
      form: z.object({
        provider: z.enum(['formspree', 'netlify', 'custom', 'none']).default('none'),
        endpoint: z.string().default(''),
      }),
      /** Path under /public; omit to hide the CV download. */
      cvPath: z.string().startsWith('/').optional(),
      hero: z.object({
        headline: z.object({ lv: z.tuple([z.string(), z.string()]), en: z.tuple([z.string(), z.string()]) }),
        intro: localized,
        media: z.discriminatedUnion('type', [
          z.object({ type: z.literal('image'), src: image(), alt: localized }),
          z.object({
            type: z.literal('video'),
            src: z.string().startsWith('/'),
            webm: z.string().startsWith('/').optional(),
            poster: image(),
            alt: localized,
          }),
        ]),
        caption: localized.optional(),
      }),
      about: z.object({
        portrait: image(),
        portraitAlt: localized,
        teaserPortrait: image(),
        teaserPortraitAlt: localized,
        lead: localized,
        bio: localized,
        teaser: localized,
        principles: z.array(z.object({ title: localized, text: localized })).min(1).max(6),
        expertise: z.array(localized),
      }),
      ogImage: z.string().startsWith('/'),
    }),
});

export const collections = { projects, publications, experience, education, testimonials, site };
