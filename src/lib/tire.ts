export interface ParsedTireSize {
  width: number;
  aspectRatio: number;
  rimDiameter: number;
  construction: string;
}

export function parseTireSize(size: string): ParsedTireSize | null {
  const normalized = size.replace(/\s+/g, " ").trim();
  const match = normalized.match(/(\d{3})\/(\d{2})\s*([A-Z])?\s*(\d{2})/i);
  if (!match) return null;

  return {
    width: Number(match[1]),
    aspectRatio: Number(match[2]),
    construction: match[3]?.toUpperCase() || "R",
    rimDiameter: Number(match[4]),
  };
}

export function tireSidewallMm(parsed: ParsedTireSize): number {
  return (parsed.width * parsed.aspectRatio) / 100;
}

export function tireOverallDiameterMm(parsed: ParsedTireSize): number {
  return tireSidewallMm(parsed) * 2 + parsed.rimDiameter * 25.4;
}

export function tireCircumferenceMm(parsed: ParsedTireSize): number {
  return tireOverallDiameterMm(parsed) * Math.PI;
}

export function tireRevolutionsPerKm(parsed: ParsedTireSize): number {
  return 1_000_000 / tireCircumferenceMm(parsed);
}
