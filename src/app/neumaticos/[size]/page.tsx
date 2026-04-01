import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import GatedLink from "@/components/GatedLink";
import { getModel, getTireSize, isPublished } from "@/lib/data";
import {
  parseTireSize,
  tireCircumferenceMm,
  tireOverallDiameterMm,
  tireRevolutionsPerKm,
  tireSidewallMm,
} from "@/lib/tire";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ size: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { size } = await params;
  const tireSize = getTireSize(size);
  if (!tireSize || !isPublished(tireSize.publishedAt)) return {};

  return {
    title: `${tireSize.size}: coches compatibles, diámetro y equivalencias`,
    description: `Ficha de la medida ${tireSize.size} con diámetro exterior, flanco, revoluciones por kilómetro y vehículos que la utilizan de serie.`,
  };
}

function StatCard({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-4">
      <div className="text-xs uppercase tracking-wide text-gray-500">{label}</div>
      <div className="text-2xl font-bold text-gray-900 mt-1">{value}</div>
      {note ? <div className="text-xs text-gray-500 mt-1">{note}</div> : null}
    </div>
  );
}

export default async function TireSizePage({ params }: Props) {
  const { size } = await params;
  const tireSize = getTireSize(size);
  if (!tireSize || !isPublished(tireSize.publishedAt)) notFound();

  const parsed = parseTireSize(tireSize.size);
  const uniqueBrands = Array.from(new Set(tireSize.vehicles.map((vehicle) => vehicle.brand)));
  const uniqueModels = Array.from(new Set(tireSize.vehicles.map((vehicle) => `${vehicle.brand} ${vehicle.model}`)));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <Link href="/neumaticos" className="hover:text-blue-600">Neumáticos</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">{tireSize.size}</span>
      </nav>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr] mb-8">
        <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8">
          <div className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 mb-4">
            Medida de neumático
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">{tireSize.size}</h1>
          <p className="text-gray-600 leading-relaxed">
            Esta ficha resume la medida {tireSize.size}, utilizada por {tireSize.vehicles.length.toLocaleString("es-ES")} vehículos
            de {uniqueBrands.length} marcas en la base de datos. Incluye dimensiones teóricas del neumático y una lista de modelos
            que la montan de origen.
          </p>
        </div>

        <div className="rounded-3xl border border-blue-200 bg-blue-50 p-6">
          <h2 className="font-semibold text-blue-900 mb-3">Resumen de compatibilidad</h2>
          <ul className="space-y-2 text-sm text-blue-900/90">
            <li>• {uniqueBrands.length} marcas representadas</li>
            <li>• {uniqueModels.length} combinaciones marca-modelo</li>
            <li>• Páginas enlazadas solo cuando la ficha del vehículo está publicada</li>
            <li>• Verifica siempre carga, velocidad y homologación antes de cambiar de medida</li>
          </ul>
        </div>
      </div>

      {parsed ? (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <StatCard label="Ancho" value={`${parsed.width} mm`} />
          <StatCard label="Perfil" value={`${parsed.aspectRatio}%`} />
          <StatCard label="Diámetro de llanta" value={`${parsed.rimDiameter}″`} />
          <StatCard label="Construcción" value={parsed.construction} />
          <StatCard label="Flanco" value={`${Math.round(tireSidewallMm(parsed))} mm`} />
          <StatCard label="Diámetro exterior" value={`${Math.round(tireOverallDiameterMm(parsed))} mm`} />
          <StatCard label="Circunferencia" value={`${Math.round(tireCircumferenceMm(parsed))} mm`} />
          <StatCard label="Vueltas por km" value={`${Math.round(tireRevolutionsPerKm(parsed))}`} note="Aproximación teórica" />
        </div>
      ) : null}

      <div className="rounded-3xl border border-gray-200 bg-white p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Vehículos que usan {tireSize.size}</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="py-3 pr-4 font-medium">Marca</th>
                <th className="py-3 pr-4 font-medium">Modelo</th>
                <th className="py-3 pr-4 font-medium">Años</th>
                <th className="py-3 pr-4 font-medium">Variante</th>
                <th className="py-3 font-medium">Ficha</th>
              </tr>
            </thead>
            <tbody>
              {tireSize.vehicles.map((vehicle, index) => {
                const modelMatch = getModel(vehicle.brandSlug, vehicle.modelSlug);
                const published = modelMatch ? isPublished(modelMatch.model.publishedAt) : false;
                return (
                  <tr key={`${vehicle.brandSlug}-${vehicle.modelSlug}-${vehicle.variant}-${index}`} className="border-b border-gray-100">
                    <td className="py-3 pr-4 font-medium text-gray-900">{vehicle.brand}</td>
                    <td className="py-3 pr-4 text-gray-700">{vehicle.model}</td>
                    <td className="py-3 pr-4 text-gray-600">{vehicle.years}</td>
                    <td className="py-3 pr-4 text-gray-600">{vehicle.variant}</td>
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
        <h2 className="text-xl font-bold text-gray-900 mb-3">Qué significa la medida {tireSize.size}</h2>
        <div className="space-y-3 text-gray-600 leading-relaxed">
          <p>
            El primer número indica el ancho del neumático en milímetros. El segundo expresa la relación de aspecto,
            es decir, la altura del flanco como porcentaje del ancho. La letra central identifica la construcción,
            normalmente radial, y el último número corresponde al diámetro interior compatible con la llanta.
          </p>
          <p>
            Si estás valorando una equivalencia, no basta con comparar el ancho. Debes revisar el diámetro total,
            el índice de carga, el código de velocidad y la homologación admitida por el fabricante y la ITV.
          </p>
          <p className="text-xs text-gray-400 italic">
            Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
          </p>
        </div>
      </div>
    </div>
  );
}
