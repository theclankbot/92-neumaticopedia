import Link from "next/link";
import GatedLink from "@/components/GatedLink";
import VehicleFinder from "@/components/VehicleFinder";
import {
  getAllBrands,
  getAllPressureGuides,
  getAllTireSizes,
  getVehicleCounts,
  getVehicleFinderData,
  isPublished,
} from "@/lib/data";

export const dynamic = "force-dynamic";

const COUNTRY_FLAGS: Record<string, string> = {
  "Japón": "🇯🇵",
  "Alemania": "🇩🇪",
  "España": "🇪🇸",
  "Corea del Sur": "🇰🇷",
  "Francia": "🇫🇷",
  "Estados Unidos": "🇺🇸",
  "Rumanía": "🇷🇴",
  "Italia": "🇮🇹",
  "República Checa": "🇨🇿",
  "Suecia": "🇸🇪",
  "Reino Unido": "🇬🇧",
  "Reino Unido/China": "🇬🇧",
};

export default function HomePage() {
  const brands = getAllBrands();
  const finderData = getVehicleFinderData();
  const counts = getVehicleCounts();
  const tireSizes = getAllTireSizes().slice(0, 8);
  const pressureGuides = getAllPressureGuides().slice(0, 10);
  const popularBrands = brands.slice(0, 12);

  return (
    <>
      <section className="bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white py-14 md:py-20">
        <div className="max-w-7xl mx-auto px-4 grid gap-10 lg:grid-cols-[1.1fr_0.9fr] items-center">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-100 mb-4">
              Base de datos española de neumáticos y llantas
            </div>
            <h1 className="text-3xl md:text-5xl font-bold leading-tight mb-4">
              Encuentra los neumáticos de tu coche
            </h1>
            <p className="text-lg md:text-xl text-slate-300 max-w-2xl mb-6">
              Consulta medidas OEM, patrones PCD, presión recomendada y fichas técnicas de {counts.brandCount} marcas,
              {" "}{counts.modelCount.toLocaleString("es-ES")} modelos y {counts.variantCount.toLocaleString("es-ES")} variantes.
            </p>
            <div className="flex flex-wrap gap-3 mb-8">
              <Link
                href="/marcas"
                className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-500"
              >
                Explorar marcas
              </Link>
              <Link
                href="/equivalencia-neumaticos"
                className="rounded-xl border border-white/15 px-5 py-3 font-semibold text-white transition hover:bg-white/10"
              >
                Calcular equivalencias
              </Link>
              <Link
                href="/presion-neumaticos"
                className="rounded-xl border border-blue-300/25 px-5 py-3 font-semibold text-blue-100 transition hover:bg-blue-500/10"
              >
                Guías de presión
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-2xl font-bold text-white">{counts.brandCount}</div>
                <div className="text-slate-400">marcas</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-2xl font-bold text-white">{counts.modelCount.toLocaleString("es-ES")}</div>
                <div className="text-slate-400">modelos</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-2xl font-bold text-white">{counts.variantCount.toLocaleString("es-ES")}</div>
                <div className="text-slate-400">variantes</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-2xl font-bold text-white">{counts.tireSizeCount}</div>
                <div className="text-slate-400">medidas de neumático</div>
              </div>
            </div>
          </div>

          <VehicleFinder data={finderData} />
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex items-end justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Marcas destacadas</h2>
            <p className="text-gray-600 mt-1">Accede por fabricante para ver modelos, generaciones, variantes y medidas OEM.</p>
          </div>
          <Link href="/marcas" className="text-sm font-semibold text-blue-600 hover:text-blue-800">
            Ver todas las marcas →
          </Link>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {popularBrands.map((brand) => (
            <GatedLink
              key={brand.slug}
              href={`/${brand.slug}`}
              published={isPublished(brand.publishedAt)}
              className="block"
              publishedClassName="group"
            >
              <div
                className={`rounded-2xl border p-4 h-full transition-all ${
                  isPublished(brand.publishedAt)
                    ? "bg-white border-gray-200 hover:border-blue-300 hover:shadow-md"
                    : "bg-gray-50 border-gray-100"
                }`}
              >
                <div className="text-2xl mb-2">{COUNTRY_FLAGS[brand.country] || "🚗"}</div>
                <div className={`font-semibold ${isPublished(brand.publishedAt) ? "text-gray-900" : "text-gray-500"}`}>
                  {brand.name}
                </div>
                <div className="text-xs text-gray-500 mt-1">{brand.modelCount} modelos</div>
              </div>
            </GatedLink>
          ))}
        </div>
      </section>

      <section className="bg-white border-y border-gray-200 py-12">
        <div className="max-w-7xl mx-auto px-4 grid gap-8 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Medidas de neumáticos más consultadas</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {tireSizes.map((size) => (
                <GatedLink
                  key={size.slug}
                  href={`/neumaticos/${size.slug}`}
                  published={isPublished(size.publishedAt)}
                  className="rounded-2xl border p-4 block"
                  publishedClassName="border-blue-200 bg-blue-50 hover:bg-blue-100/60"
                  unpublishedClassName="border-gray-200 bg-gray-50"
                >
                  <div className="font-mono font-semibold text-gray-900">{size.size}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {size.vehicles.length.toLocaleString("es-ES")} vehículos en la base de datos
                  </div>
                </GatedLink>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Guías rápidas de presión</h2>
            <div className="space-y-3">
              {pressureGuides.map(({ brand, model }) => (
                <GatedLink
                  key={`${brand.slug}-${model.slug}`}
                  href={`/presion-neumaticos/${brand.slug}/${model.slug}`}
                  published={isPublished(model.publishedAt)}
                  className="flex items-center justify-between rounded-2xl border p-4"
                  publishedClassName="border-amber-200 bg-amber-50 hover:bg-amber-100/60"
                  unpublishedClassName="border-gray-200 bg-gray-50"
                >
                  <div>
                    <div className="font-semibold text-gray-900">{brand.name} {model.name}</div>
                    <div className="text-sm text-gray-600">{model.years} • {model.bodyType}</div>
                  </div>
                  <span className="text-sm font-semibold text-amber-700">Presión →</span>
                </GatedLink>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid gap-6 lg:grid-cols-3">
          <Link href="/equivalencia-neumaticos" className="group rounded-3xl border border-blue-200 bg-gradient-to-br from-blue-50 to-white p-6 hover:shadow-md transition">
            <div className="text-3xl mb-3">🔄</div>
            <h2 className="text-lg font-semibold text-gray-900 group-hover:text-blue-700">Calculadora de equivalencias</h2>
            <p className="text-sm text-gray-600 mt-2">Compara dos medidas y comprueba diferencias de diámetro, desarrollo y desviación para ITV.</p>
          </Link>
          <Link href="/pcd" className="group rounded-3xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-white p-6 hover:shadow-md transition">
            <div className="text-3xl mb-3">⚙️</div>
            <h2 className="text-lg font-semibold text-gray-900 group-hover:text-emerald-700">Patrones PCD por coche</h2>
            <p className="text-sm text-gray-600 mt-2">Explora patrones de anclaje, diámetro de buje y compatibilidades por marca, modelo y llanta.</p>
          </Link>
          <Link href="/fuentes-de-datos" className="group rounded-3xl border border-amber-200 bg-gradient-to-br from-amber-50 to-white p-6 hover:shadow-md transition">
            <div className="text-3xl mb-3">📚</div>
            <h2 className="text-lg font-semibold text-gray-900 group-hover:text-amber-700">Fuentes y metodología</h2>
            <p className="text-sm text-gray-600 mt-2">Documentamos cada origen de datos, fecha de captura y cómo cruzamos wheel-size, NHTSA y Wikimedia.</p>
          </Link>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 pb-14">
        <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Tu guía completa de neumáticos y llantas por coche</h2>
          <div className="grid gap-4 text-gray-600 leading-relaxed md:grid-cols-2">
            <p>
              Neumaticopedia organiza la información por marca, modelo, año y variante para responder a búsquedas como
              “qué neumáticos lleva mi coche”, “presión Toyota Corolla” o “PCD 5x112 qué coches lo usan”. Cada ficha
              agrupa dimensiones del vehículo, medidas OEM, llantas compatibles, par de apriete y datos de presión.
            </p>
            <p>
              También publicamos páginas inversas por medida de neumático y por patrón PCD para que puedas descubrir
              qué vehículos comparten una misma configuración. Esto es útil si buscas llantas compatibles, comparar
              alternativas o validar equivalencias antes de pasar ITV.
            </p>
            <p>
              La base de datos se construye con listados de modelos de wheel-size.com, referencias cruzadas con la API
              vPIC de NHTSA y enriquecimiento visual desde Wikimedia Commons. Cuando una ficha todavía no está publicada,
              la mostramos como “Próximamente” para evitar enlaces rotos y mantener una publicación progresiva ordenada.
            </p>
            <p>
              Las medidas y presiones mostradas son orientativas y deben verificarse siempre con el manual del vehículo,
              la pegatina de presión del fabricante o un profesional especializado. Para consultas críticas de seguridad,
              prioriza siempre la documentación oficial de la marca.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
