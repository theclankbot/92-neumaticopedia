import type { Metadata } from "next";
import Link from "next/link";
import GatedLink from "@/components/GatedLink";
import { getAllPressureGuides, isPublished } from "@/lib/data";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Guías de presión de neumáticos por coche",
  description:
    "Índice de guías de presión de neumáticos por marca y modelo con referencias para carga normal y carga completa.",
};

export default function PressureIndexPage() {
  const guides = getAllPressureGuides();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Presión de neumáticos</span>
      </nav>

      <div className="max-w-3xl mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Guías de presión de neumáticos</h1>
        <p className="text-gray-600 leading-relaxed">
          Consulta la presión recomendada por marca y modelo. Cada guía reúne las variantes del vehículo, presiones con carga normal
          y carga completa, tamaños de neumático montados y acceso a las fichas completas cuando están publicadas.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {guides.map(({ brand, model }) => {
          const firstVariant = model.generations[0]?.variants[0];
          return (
            <GatedLink
              key={`${brand.slug}-${model.slug}`}
              href={`/presion-neumaticos/${brand.slug}/${model.slug}`}
              published={isPublished(model.publishedAt)}
              className="block rounded-2xl border p-5"
              publishedClassName="border-amber-200 bg-amber-50 hover:bg-amber-100/60"
              unpublishedClassName="border-gray-200 bg-gray-50"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="font-semibold text-gray-900 text-lg">{brand.name} {model.name}</h2>
                  <p className="text-sm text-gray-600 mt-1">{model.years} • {model.bodyType}</p>
                </div>
                <div className="rounded-full bg-white/80 px-3 py-1 text-xs font-semibold text-amber-700">
                  {model.generations.reduce((count, generation) => count + generation.variants.length, 0)} variantes
                </div>
              </div>
              {firstVariant ? (
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                  <div className="rounded-xl bg-white/80 p-3">
                    <div className="text-gray-500 text-xs uppercase">Delante</div>
                    <div className="font-semibold text-gray-900 mt-1">{firstVariant.tirePressureFrontBar.toLocaleString("es-ES", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bar</div>
                  </div>
                  <div className="rounded-xl bg-white/80 p-3">
                    <div className="text-gray-500 text-xs uppercase">Detrás</div>
                    <div className="font-semibold text-gray-900 mt-1">{firstVariant.tirePressureRearBar.toLocaleString("es-ES", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bar</div>
                  </div>
                </div>
              ) : null}
            </GatedLink>
          );
        })}
      </div>
    </div>
  );
}
