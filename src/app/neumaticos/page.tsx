import type { Metadata } from "next";
import Link from "next/link";
import GatedLink from "@/components/GatedLink";
import { getAllTireSizes, isPublished } from "@/lib/data";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Medidas de neumáticos por tamaño",
  description:
    "Índice de medidas de neumáticos con vehículos que usan cada tamaño, equivalencias y páginas detalladas por medida.",
};

export default function TireSizesIndexPage() {
  const tireSizes = getAllTireSizes();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Neumáticos</span>
      </nav>

      <div className="max-w-3xl mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Medidas de neumáticos</h1>
        <p className="text-gray-600 leading-relaxed">
          Explora la base de datos inversa por tamaño. Cada página de medida reúne los vehículos que la utilizan,
          el diámetro exterior estimado, el flanco y el número de vueltas por kilómetro para facilitar comparativas.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {tireSizes.map((size) => (
          <GatedLink
            key={size.slug}
            href={`/neumaticos/${size.slug}`}
            published={isPublished(size.publishedAt)}
            className="block rounded-2xl border p-5"
            publishedClassName="border-blue-200 bg-blue-50 hover:bg-blue-100/60"
            unpublishedClassName="border-gray-200 bg-gray-50"
          >
            <div className="font-mono text-lg font-semibold text-gray-900">{size.size}</div>
            <div className="text-sm text-gray-600 mt-2">
              {size.vehicles.length.toLocaleString("es-ES")} vehículos en la base de datos
            </div>
            <div className="text-xs text-gray-500 mt-3">
              Marcas destacadas: {Array.from(new Set(size.vehicles.map((vehicle) => vehicle.brand))).slice(0, 4).join(", ")}
            </div>
          </GatedLink>
        ))}
      </div>
    </div>
  );
}
