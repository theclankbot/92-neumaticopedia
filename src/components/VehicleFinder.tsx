"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { FinderBrand } from "@/lib/data";

interface Props {
  data: FinderBrand[];
}

export default function VehicleFinder({ data }: Props) {
  const router = useRouter();
  const [brandSlug, setBrandSlug] = useState("");
  const [modelSlug, setModelSlug] = useState("");
  const [yearSlug, setYearSlug] = useState("");
  const [variantSlug, setVariantSlug] = useState("");

  const selectedBrand = useMemo(
    () => data.find((brand) => brand.slug === brandSlug) || null,
    [data, brandSlug],
  );
  const selectedModel = useMemo(
    () => selectedBrand?.models.find((model) => model.slug === modelSlug) || null,
    [selectedBrand, modelSlug],
  );
  const selectedYear = useMemo(
    () => selectedModel?.years.find((year) => year.slug === yearSlug) || null,
    [selectedModel, yearSlug],
  );
  const selectedVariant = useMemo(
    () => selectedYear?.variants.find((variant) => variant.slug === variantSlug) || null,
    [selectedYear, variantSlug],
  );

  const detailHref =
    selectedBrand && selectedModel && selectedYear && selectedVariant
      ? `/${selectedBrand.slug}/${selectedModel.slug}/${selectedYear.slug}/${selectedVariant.slug}`
      : "";

  const pressureHref =
    selectedBrand && selectedModel ? `/presion-neumaticos/${selectedBrand.slug}/${selectedModel.slug}` : "";

  return (
    <div className="rounded-2xl border border-white/15 bg-white/10 backdrop-blur p-4 md:p-6 text-left shadow-2xl">
      <div className="flex items-center gap-2 mb-4">
        <div className="h-10 w-10 rounded-full bg-blue-500/20 flex items-center justify-center text-xl">🧭</div>
        <div>
          <h2 className="text-lg md:text-xl font-semibold text-white">Buscador por vehículo</h2>
          <p className="text-sm text-blue-100/80">Marca → modelo → año → variante</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <label className="space-y-1">
          <span className="text-xs uppercase tracking-wide text-blue-100/70">Marca</span>
          <select
            value={brandSlug}
            onChange={(event) => {
              setBrandSlug(event.target.value);
              setModelSlug("");
              setYearSlug("");
              setVariantSlug("");
            }}
            className="w-full rounded-xl border border-white/15 bg-slate-950/50 px-3 py-3 text-sm text-white outline-none focus:border-blue-400"
          >
            <option value="">Selecciona marca</option>
            {data.map((brand) => (
              <option key={brand.slug} value={brand.slug}>
                {brand.name}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-1">
          <span className="text-xs uppercase tracking-wide text-blue-100/70">Modelo</span>
          <select
            value={modelSlug}
            disabled={!selectedBrand}
            onChange={(event) => {
              setModelSlug(event.target.value);
              setYearSlug("");
              setVariantSlug("");
            }}
            className="w-full rounded-xl border border-white/15 bg-slate-950/50 px-3 py-3 text-sm text-white outline-none focus:border-blue-400 disabled:opacity-50"
          >
            <option value="">Selecciona modelo</option>
            {selectedBrand?.models.map((model) => (
              <option key={model.slug} value={model.slug}>
                {model.name}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-1">
          <span className="text-xs uppercase tracking-wide text-blue-100/70">Año / generación</span>
          <select
            value={yearSlug}
            disabled={!selectedModel}
            onChange={(event) => {
              setYearSlug(event.target.value);
              setVariantSlug("");
            }}
            className="w-full rounded-xl border border-white/15 bg-slate-950/50 px-3 py-3 text-sm text-white outline-none focus:border-blue-400 disabled:opacity-50"
          >
            <option value="">Selecciona año</option>
            {selectedModel?.years.map((year) => (
              <option key={year.slug} value={year.slug}>
                {year.name}
              </option>
            ))}
          </select>
        </label>

        <label className="space-y-1">
          <span className="text-xs uppercase tracking-wide text-blue-100/70">Variante</span>
          <select
            value={variantSlug}
            disabled={!selectedYear}
            onChange={(event) => setVariantSlug(event.target.value)}
            className="w-full rounded-xl border border-white/15 bg-slate-950/50 px-3 py-3 text-sm text-white outline-none focus:border-blue-400 disabled:opacity-50"
          >
            <option value="">Selecciona variante</option>
            {selectedYear?.variants.map((variant) => (
              <option key={variant.slug} value={variant.slug}>
                {variant.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="mt-4 flex flex-col lg:flex-row lg:items-center gap-3">
        <button
          type="button"
          disabled={!detailHref || !selectedVariant || !selectedVariant.publishedAt}
          onClick={() => router.push(detailHref)}
          className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700"
        >
          Ver ficha completa
        </button>
        <button
          type="button"
          disabled={!pressureHref || !selectedModel?.publishedAt}
          onClick={() => router.push(pressureHref)}
          className="rounded-xl border border-white/20 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Ver presión recomendada
        </button>
        {selectedVariant && !selectedVariant.publishedAt ? (
          <span className="text-xs text-amber-200">La ficha detallada de esta variante se publicará progresivamente. Puedes consultar la guía de presión del modelo.</span>
        ) : (
          <span className="text-xs text-blue-100/75">Busca por modelo para comparar neumáticos OEM, PCD, presiones y especificaciones técnicas.</span>
        )}
      </div>
    </div>
  );
}
