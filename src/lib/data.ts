import fs from "fs";
import path from "path";

const DATA_DIR = path.join(process.cwd(), "data");

export interface Brand {
  slug: string;
  name: string;
  country: string;
  founded: string;
  hq: string;
  description: string;
  modelCount: number;
  publishedAt: string | null;
}

export interface Variant {
  slug: string;
  name: string;
  engineCode: string;
  displacement: number;
  fuelType: string;
  powerHp: number;
  powerKw: number;
  torqueNm: number;
  transmission: string;
  gears: number;
  driveType: string;
  lengthMm: number;
  widthMm: number;
  heightMm: number;
  wheelbaseMm: number;
  weightKg: number;
  grossWeightKg: number;
  trunkCapacityL: number;
  fuelTankL: number;
  consumption: number;
  co2: number;
  topSpeed: number;
  acceleration0100: number;
  tireSizeFront: string;
  tireSizeRear: string;
  rimSize: string;
  pcd: string;
  centerBore: number;
  offsetMin: number;
  offsetMax: number;
  wheelTorqueNm: number;
  threadSize: string;
  boltType: string;
  tirePressureFrontBar: number;
  tirePressureRearBar: number;
  tirePressureFrontLoadedBar: number;
  tirePressureRearLoadedBar: number;
  publishedAt: string | null;
}

export interface Generation {
  slug: string;
  name: string;
  yearStart: number;
  yearEnd: number;
  publishedAt: string | null;
  variants: Variant[];
}

export interface Model {
  slug: string;
  name: string;
  bodyType: string;
  segment: string;
  years: string;
  current: boolean;
  publishedAt: string | null;
  generations: Generation[];
  imageUrl?: string | null;
  imagePageUrl?: string | null;
  imageTitle?: string | null;
  imageLicense?: string | null;
  imageFetchedAt?: string | null;
  wheelSizeKnown?: boolean;
}

export interface BrandFull extends Brand {
  models: Model[];
}

export interface TireVehicleReference {
  brand: string;
  brandSlug: string;
  model: string;
  modelSlug: string;
  variant: string;
  years: string;
}

export interface TireSize {
  size: string;
  slug: string;
  publishedAt: string | null;
  vehicles: TireVehicleReference[];
}

export interface PCDVehicleReference {
  brand: string;
  brandSlug: string;
  model: string;
  modelSlug: string;
  years: string;
}

export interface PCDPattern {
  pattern: string;
  slug: string;
  publishedAt: string | null;
  vehicles: PCDVehicleReference[];
}

export interface FinderVariant {
  slug: string;
  name: string;
  publishedAt: string | null;
}

export interface FinderYear {
  slug: string;
  name: string;
  publishedAt: string | null;
  variants: FinderVariant[];
}

export interface FinderModel {
  slug: string;
  name: string;
  publishedAt: string | null;
  years: FinderYear[];
}

export interface FinderBrand {
  slug: string;
  name: string;
  publishedAt: string | null;
  models: FinderModel[];
}

export interface SourceMetadata {
  generatedAt: string;
  wheelSize: Record<string, {
    brand: string;
    sourceUrl: string;
    modelCount: number;
    sampleModels: string[];
    fetchedAt: string;
    license: string;
  }>;
  nhtsa: Record<string, {
    make: string;
    count: number;
    models: string[];
    sourceUrl: string;
    fetchedAt: string;
    error?: string;
  }>;
  wikipedia: {
    api: string;
    fetchedAt: string;
    license: string;
  };
}

function readJSON<T>(filename: string): T {
  const filepath = path.join(DATA_DIR, filename);
  const raw = fs.readFileSync(filepath, "utf-8");
  return JSON.parse(raw) as T;
}

export function isPublished(publishedAt: string | null): boolean {
  if (!publishedAt) return false;
  return new Date(publishedAt) <= new Date();
}

export function getAllBrands(): Brand[] {
  return readJSON<Brand[]>("brands.json");
}

export function getBrand(slug: string): BrandFull | null {
  try {
    return readJSON<BrandFull>(`brand-${slug}.json`);
  } catch {
    return null;
  }
}

export function getModel(brandSlug: string, modelSlug: string): { brand: BrandFull; model: Model } | null {
  const brand = getBrand(brandSlug);
  if (!brand) return null;
  const model = brand.models.find((entry) => entry.slug === modelSlug);
  if (!model) return null;
  return { brand, model };
}

export function getAllTireSizes(): TireSize[] {
  return readJSON<TireSize[]>("tire-sizes.json");
}

export function getTireSize(slug: string): TireSize | null {
  return getAllTireSizes().find((entry) => entry.slug === slug) || null;
}

export function getAllPCDPatterns(): PCDPattern[] {
  return readJSON<PCDPattern[]>("pcd-patterns.json");
}

export function getPCDPattern(slug: string): PCDPattern | null {
  return getAllPCDPatterns().find((entry) => entry.slug === slug) || null;
}

export function getVehicleFinderData(): FinderBrand[] {
  return readJSON<FinderBrand[]>("vehicle-finder.json");
}

export function getSourceMetadata(): SourceMetadata {
  return readJSON<SourceMetadata>("source-metadata.json");
}

export function getPressureGuide(brandSlug: string, modelSlug: string) {
  const result = getModel(brandSlug, modelSlug);
  if (!result) return null;
  const { brand, model } = result;
  const generations = model.generations.map((generation) => ({
    ...generation,
    variants: generation.variants.map((variant) => ({
      ...variant,
      detailUrl: `/${brand.slug}/${model.slug}/${generation.slug}/${variant.slug}`,
    })),
  }));

  return {
    brand,
    model,
    generations,
  };
}

export function getAllPressureGuides() {
  return getAllBrands().flatMap((brandIndex) => {
    const brand = getBrand(brandIndex.slug);
    if (!brand) return [] as Array<{ brand: BrandFull; model: Model }>;
    return brand.models.map((model) => ({ brand, model }));
  });
}

export function getVehicleCounts() {
  const brands = getAllBrands();
  let modelCount = 0;
  let variantCount = 0;

  for (const brandIndex of brands) {
    const brand = getBrand(brandIndex.slug);
    if (!brand) continue;
    for (const model of brand.models) {
      modelCount += 1;
      for (const generation of model.generations) {
        variantCount += generation.variants.length;
      }
    }
  }

  return {
    brandCount: brands.length,
    modelCount,
    variantCount,
    tireSizeCount: getAllTireSizes().length,
    pcdCount: getAllPCDPatterns().length,
  };
}

export function formatNumber(num: number): string {
  if (!Number.isFinite(num)) return "0";
  if (num === 0) return "0";
  return num.toLocaleString("es-ES");
}

export function formatDecimal(num: number, decimals = 1): string {
  return num.toLocaleString("es-ES", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}
