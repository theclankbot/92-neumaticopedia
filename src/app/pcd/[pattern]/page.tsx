import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import GatedLink from "@/components/GatedLink";
import { getModel, getPCDPattern, isPublished } from "@/lib/data";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ pattern: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { pattern } = await params;
  const pcd = getPCDPattern(pattern);
  if (!pcd || !isPublished(pcd.publishedAt)) return {};

  return {
    title: `PCD ${pcd.pattern}: coches compatibles y guía de anclaje`,
    description: `Ficha del patrón PCD ${pcd.pattern} con vehículos compatibles, marcas que lo utilizan y guía básica de anclaje de llantas.`,
  };
}

export default async function PcdPatternPage({ params }: Props) {
  const { pattern } = await params;
  const pcd = getPCDPattern(pattern);
  if (!pcd || !isPublished(pcd.publishedAt)) notFound();

  const brandCount = new Set(pcd.vehicles.map((vehicle) => vehicle.brand)).size;
  const modelCount = new Set(pcd.vehicles.map((vehicle) => `${vehicle.brandSlug}/${vehicle.modelSlug}`)).size;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <Link href="/pcd" className="hover:text-blue-600">PCD</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">{pcd.pattern}</span>
      </nav>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr] mb-8">
        <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8">
          <div className="inline-flex rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 mb-4">
            Patrón de anclaje
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">PCD {pcd.pattern}</h1>
          <p className="text-gray-600 leading-relaxed">
            El patrón {pcd.pattern} aparece en {pcd.vehicles.length.toLocaleString("es-ES")} vehículos y {brandCount} marcas de la base de datos.
            Esta página te ayuda a identificar coches que comparten anclaje para estudiar compatibilidad de llantas.
          </p>
        </div>

        <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6">
          <h2 className="font-semibold text-emerald-900 mb-3">Claves rápidas</h2>
          <ul className="space-y-2 text-sm text-emerald-900/90">
            <li>• {brandCount} marcas registradas</li>
            <li>• {modelCount} combinaciones marca-modelo</li>
            <li>• Comprueba también buje, offset y longitud de tornillería</li>
            <li>• La coincidencia del PCD no garantiza compatibilidad total de la llanta</li>
          </ul>
        </div>
      </div>

      <div className="rounded-3xl border border-gray-200 bg-white p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Vehículos con PCD {pcd.pattern}</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="py-3 pr-4 font-medium">Marca</th>
                <th className="py-3 pr-4 font-medium">Modelo</th>
                <th className="py-3 pr-4 font-medium">Años</th>
                <th className="py-3 font-medium">Ficha</th>
              </tr>
            </thead>
            <tbody>
              {pcd.vehicles.map((vehicle, index) => {
                const modelMatch = getModel(vehicle.brandSlug, vehicle.modelSlug);
                const published = modelMatch ? isPublished(modelMatch.model.publishedAt) : false;
                return (
                  <tr key={`${vehicle.brandSlug}-${vehicle.modelSlug}-${index}`} className="border-b border-gray-100">
                    <td className="py-3 pr-4 font-medium text-gray-900">{vehicle.brand}</td>
                    <td className="py-3 pr-4 text-gray-700">{vehicle.model}</td>
                    <td className="py-3 pr-4 text-gray-600">{vehicle.years}</td>
                    <td className="py-3">
                      <GatedLink
                        href={`/${vehicle.brandSlug}/${vehicle.modelSlug}`}
                        published={published}
                        publishedClassName="text-blue-600 hover:text-blue-800"
                      >
                        Ver modelo
                      </GatedLink>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="rounded-3xl border border-gray-200 bg-white p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-3">Cómo interpretar un patrón PCD</h2>
        <div className="space-y-3 text-gray-600 leading-relaxed">
          <p>
            PCD significa “Pitch Circle Diameter”. En un formato como {pcd.pattern}, el primer número indica el número de
            tornillos o espárragos y el segundo el diámetro, en milímetros, de la circunferencia imaginaria que los une.
          </p>
          <p>
            Para cambiar de llanta no basta con que coincida el PCD. También debes verificar el diámetro del buje,
            el offset (ET), el ancho de la llanta, la tornillería y el espacio libre respecto a pinzas de freno y suspensión.
          </p>
          <p className="text-xs text-gray-400 italic">
            Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
          </p>
        </div>
      </div>
    </div>
  );
}
