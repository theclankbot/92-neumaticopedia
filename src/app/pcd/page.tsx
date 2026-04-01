import type { Metadata } from "next";
import Link from "next/link";
import GatedLink from "@/components/GatedLink";
import { getAllPCDPatterns, isPublished } from "@/lib/data";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Patrones PCD por coche",
  description:
    "Índice de patrones PCD o anclaje de llantas con vehículos compatibles por marca y modelo.",
};

export default function PcdIndexPage() {
  const patterns = getAllPCDPatterns();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">PCD</span>
      </nav>

      <div className="max-w-3xl mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Patrones PCD</h1>
        <p className="text-gray-600 leading-relaxed">
          Recorre los patrones de anclaje más usados por la base de datos. Cada ficha PCD muestra qué coches lo utilizan,
          cuántas marcas aparecen y enlaces a las páginas detalladas de los modelos publicados.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {patterns.map((pattern) => (
          <GatedLink
            key={pattern.slug}
            href={`/pcd/${pattern.slug}`}
            published={isPublished(pattern.publishedAt)}
            className="block rounded-2xl border p-5"
            publishedClassName="border-emerald-200 bg-emerald-50 hover:bg-emerald-100/60"
            unpublishedClassName="border-gray-200 bg-gray-50"
          >
            <div className="font-mono text-2xl font-semibold text-gray-900">{pattern.pattern}</div>
            <div className="text-sm text-gray-600 mt-2">
              {pattern.vehicles.length.toLocaleString("es-ES")} vehículos en la base de datos
            </div>
            <div className="text-xs text-gray-500 mt-3">
              Marcas: {Array.from(new Set(pattern.vehicles.map((vehicle) => vehicle.brand))).slice(0, 5).join(", ")}
            </div>
          </GatedLink>
        ))}
      </div>
    </div>
  );
}
