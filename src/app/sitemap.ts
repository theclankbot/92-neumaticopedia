import { MetadataRoute } from "next";
import {
  getAllBrands,
  getAllPCDPatterns,
  getAllTireSizes,
  getBrand,
  isPublished,
} from "@/lib/data";

export const dynamic = "force-dynamic";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://neumaticopedia.com";
  const now = new Date();
  const entries: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: now, changeFrequency: "weekly", priority: 1 },
    { url: `${baseUrl}/marcas`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${baseUrl}/neumaticos`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/pcd`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/presion-neumaticos`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/equivalencia-neumaticos`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${baseUrl}/sobre-nosotros`, lastModified: now, changeFrequency: "monthly", priority: 0.3 },
    { url: `${baseUrl}/fuentes-de-datos`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
  ];

  const brands = getAllBrands();
  for (const brandIndex of brands) {
    if (!isPublished(brandIndex.publishedAt)) continue;
    entries.push({
      url: `${baseUrl}/${brandIndex.slug}`,
      lastModified: now,
      changeFrequency: "weekly",
      priority: 0.8,
    });

    const brand = getBrand(brandIndex.slug);
    if (!brand) continue;

    for (const model of brand.models) {
      if (!isPublished(model.publishedAt)) continue;
      entries.push({
        url: `${baseUrl}/${brand.slug}/${model.slug}`,
        lastModified: now,
        changeFrequency: "weekly",
        priority: 0.7,
      });
      entries.push({
        url: `${baseUrl}/presion-neumaticos/${brand.slug}/${model.slug}`,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.7,
      });

      for (const generation of model.generations) {
        if (!isPublished(generation.publishedAt)) continue;
        entries.push({
          url: `${baseUrl}/${brand.slug}/${model.slug}/${generation.slug}`,
          lastModified: now,
          changeFrequency: "monthly",
          priority: 0.6,
        });

        for (const variant of generation.variants) {
          if (!isPublished(variant.publishedAt)) continue;
          entries.push({
            url: `${baseUrl}/${brand.slug}/${model.slug}/${generation.slug}/${variant.slug}`,
            lastModified: now,
            changeFrequency: "monthly",
            priority: 0.5,
          });
        }
      }
    }
  }

  for (const tireSize of getAllTireSizes()) {
    if (!isPublished(tireSize.publishedAt)) continue;
    entries.push({
      url: `${baseUrl}/neumaticos/${tireSize.slug}`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.6,
    });
  }

  for (const pcd of getAllPCDPatterns()) {
    if (!isPublished(pcd.publishedAt)) continue;
    entries.push({
      url: `${baseUrl}/pcd/${pcd.slug}`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.6,
    });
  }

  return entries;
}
