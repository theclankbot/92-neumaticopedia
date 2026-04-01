
import { Metadata } from "next";
import Link from "next/link";
import { getAllBrands, isPublished } from "@/lib/data";
import GatedLink from "@/components/GatedLink";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Todas las marcas de coches: neumáticos y medidas",
  description:
    "Directorio completo de marcas de coches con datos de neumáticos, llantas, PCD y especificaciones técnicas. Encuentra tu marca y consulta las medidas de tu vehículo.",
};

const COUNTRY_FLAGS: Record<string, string> = {
  "Japón": "🇯🇵", "Alemania": "🇩🇪", "España": "🇪🇸", "Corea del Sur": "🇰🇷",
  "Francia": "🇫🇷", "Estados Unidos": "🇺🇸", "Rumanía": "🇷🇴", "Italia": "🇮🇹",
  "República Checa": "🇨🇿", "Suecia": "🇸🇪",
};

export default function MarcasPage() {
  const brands = getAllBrands();
  const byCountry = brands.reduce<Record<string, typeof brands>>((acc, b) => {
    const c = b.country;
    if (!acc[c]) acc[c] = [];
    acc[c].push(b);
    return acc;
  }, {});

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Marcas</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">Marcas de coches</h1>
      <p className="text-gray-600 mb-8">
        Consulta las medidas de neumáticos, presión y llantas de {brands.length} marcas de coches.
        Selecciona una marca para ver todos sus modelos y especificaciones.
      </p>

      {/* All brands grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 mb-12">
        {brands.map((brand) => (
          <GatedLink
            key={brand.slug}
            href={`/${brand.slug}`}
            published={isPublished(brand.publishedAt)}
            className="block"
            publishedClassName="group"
          >
            <div className={`bg-white rounded-xl border p-5 text-center transition-all ${
              isPublished(brand.publishedAt)
                ? "border-gray-200 hover:border-blue-300 hover:shadow-md"
                : "border-gray-100 bg-gray-50"
            }`}>
              <div className="text-3xl mb-2">{COUNTRY_FLAGS[brand.country] || "🚗"}</div>
              <div className={`font-semibold ${
                isPublished(brand.publishedAt) ? "text-gray-900" : "text-gray-400"
              }`}>
                {brand.name}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {brand.modelCount} modelos • {brand.country}
              </div>
            </div>
          </GatedLink>
        ))}
      </div>

      {/* By country sections */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Marcas por país</h2>
      {Object.entries(byCountry).sort(([,a],[,b]) => b.length - a.length).map(([country, countryBrands]) => (
        <div key={country} className="mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            {COUNTRY_FLAGS[country] || ""} {country} ({countryBrands.length} marcas)
          </h3>
          <div className="flex flex-wrap gap-2">
            {countryBrands.map((b) => (
              <GatedLink
                key={b.slug}
                href={`/${b.slug}`}
                published={isPublished(b.publishedAt)}
                publishedClassName="bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200"
                unpublishedClassName="bg-gray-50 border-gray-200"
                className="px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors"
              >
                {b.name}
              </GatedLink>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

