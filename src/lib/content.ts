import { getCollection, getEntry } from 'astro:content';

export async function getSite() {
  const entry = await getEntry('site', 'site');
  if (!entry) throw new Error('Missing src/content/site/site.yaml');
  return entry.data;
}

export async function getProjects() {
  const all = await getCollection('projects');
  return all.map((e) => e.data).sort((a, b) => a.order - b.order);
}

export async function getPublications() {
  const all = await getCollection('publications');
  return all
    .map((e) => ({ id: e.id, ...e.data }))
    .sort((a, b) => b.date.getTime() - a.date.getTime());
}

export async function getExperience() {
  return (await getCollection('experience')).map((e) => e.data).sort((a, b) => a.order - b.order);
}

export async function getEducation() {
  return (await getCollection('education')).map((e) => e.data).sort((a, b) => a.order - b.order);
}

export async function getTestimonials() {
  return (await getCollection('testimonials')).map((e) => e.data).sort((a, b) => a.order - b.order);
}

export type Project = Awaited<ReturnType<typeof getProjects>>[number];
export type Publication = Awaited<ReturnType<typeof getPublications>>[number];
export type Site = Awaited<ReturnType<typeof getSite>>;
