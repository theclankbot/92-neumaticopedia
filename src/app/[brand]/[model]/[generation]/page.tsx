
import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getBrand, isPublished, formatNumber, formatDecimal } from "@/lib/data";
import GatedLink from "@/components/GatedLink";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ brand: string; model: string; generation: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { brand: bSlug, model: mSlug, generation: gSlug } = await params;
  const brand = getBrand(bSlug);
  if (!brand) return {};
  const model = brand.models.find((m) => m.slug === mSlug);
  const gen = model?.generations.find((g) => g.slug === gSlug);
  if (!model || !gen || !isPublished(gen.publishedAt)) return {};
  return {
    title: `${brand.name} ${model.name} ${gen.yearStart}-${gen.yearEnd}: neumáticos, medidas y ficha técnica`,
    description: `Medidas de neumáticos y ficha técnica completa del ${brand.name} ${model.name} ${gen.name}. ${gen.variants.length} variantes con datos de llantas, PCD, presión y especificaciones.`,
  };
}

export default async function GenerationPage({ params }: Props) {
  const { brand: bSlug, model: mSlug, generation: gSlug } = await params;
  const brand = getBrand(bSlug);
  if (!brand || !isPublished(brand.publishedAt)) notFound();
  const model = brand.models.find((m) => m.slug === mSlug);
  if (!model || !isPublished(model.publishedAt)) notFound();
  const gen = model.generations.find((g) => g.slug === gSlug);
  if (!gen || !isPublished(gen.publishedAt)) notFound();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <GatedLink href={`/${brand.slug}`} published={isPublished(brand.publishedAt)} publishedClassName="hover:text-blue-600">
          {brand.name}
        </GatedLink>
        <span className="mx-2">›</span>
        <GatedLink href={`/${brand.slug}/${model.slug}`} published={isPublished(model.publishedAt)} publishedClassName="hover:text-blue-600">
          {model.name}
        </GatedLink>
        <span className="mx-2">›</span>
        <span className="text-gray-900">{gen.yearStart}–{gen.yearEnd}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        {brand.name} {model.name} {gen.name} ({gen.yearStart}–{gen.yearEnd})
      </h1>
      <p className="text-gray-600 mb-8">
        Medidas de neumáticos, llantas y ficha técnica de las {gen.variants.length} variantes del {brand.name} {model.name} {gen.name}.
      </p>

      {/* Variants detailed */}
      {gen.variants.map((v) => (
        <div key={v.slug} className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            <GatedLink
              href={`/${brand.slug}/${model.slug}/${gen.slug}/${v.slug}`}
              published={isPublished(v.publishedAt)}
              publishedClassName="text-blue-600 hover:text-blue-800"
            >
              {v.name}
            </GatedLink>
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Tire info */}
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 mb-2 text-sm">🛞 Neumáticos</h3>
              <div className="space-y-1 text-sm">
                <div><span className="text-gray-600">Delanteros:</span> <span className="font-mono font-medium">{v.tireSizeFront}</span></div>
                <div><span className="text-gray-600">Traseros:</span> <span className="font-mono font-medium">{v.tireSizeRear || v.tireSizeFront}</span></div>
                <div><span className="text-gray-600">Llantas:</span> <span className="font-mono font-medium">{v.rimSize}</span></div>
              </div>
            </div>

            {/* Wheel specs */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2 text-sm">⚙️ Llanta</h3>
              <div className="space-y-1 text-sm">
                <div><span className="text-gray-600">PCD:</span> <span className="font-mono font-medium">{v.pcd}</span></div>
                <div><span className="text-gray-600">Buje:</span> <span className="font-mono font-medium">{v.centerBore} mm</span></div>
                <div><span className="text-gray-600">Offset:</span> <span className="font-mono font-medium">ET{v.offsetMin}–ET{v.offsetMax}</span></div>
                <div><span className="text-gray-600">Par apriete:</span> <span className="font-mono font-medium">{v.wheelTorqueNm} Nm</span></div>
              </div>
            </div>

            {/* Pressure */}
            <div className="bg-amber-50 rounded-lg p-4">
              <h3 className="font-semibold text-amber-900 mb-2 text-sm">🔧 Presión (bar)</h3>
              <div className="space-y-1 text-sm">
                <div><span className="text-gray-600">Delantero:</span> <span className="font-mono font-medium">{formatDecimal(v.tirePressureFrontBar)}</span></div>
                <div><span className="text-gray-600">Trasero:</span> <span className="font-mono font-medium">{formatDecimal(v.tirePressureRearBar)}</span></div>
                <div><span className="text-gray-600">Del. cargado:</span> <span className="font-mono font-medium">{formatDecimal(v.tirePressureFrontLoadedBar)}</span></div>
                <div><span className="text-gray-600">Tras. cargado:</span> <span className="font-mono font-medium">{formatDecimal(v.tirePressureRearLoadedBar)}</span></div>
              </div>
            </div>
          </div>

          {/* Engine & specs */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 mt-4">
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">Motor</div>
              <div className="font-mono text-sm font-medium">{v.displacement ? `${formatNumber(v.displacement)} cc` : "Eléctrico"}</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">Potencia</div>
              <div className="font-mono text-sm font-medium">{v.powerHp} CV</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">Par</div>
              <div className="font-mono text-sm font-medium">{v.torqueNm} Nm</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">Peso</div>
              <div className="font-mono text-sm font-medium">{formatNumber(v.weightKg)} kg</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">0-100</div>
              <div className="font-mono text-sm font-medium">{formatDecimal(v.acceleration0100)} s</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="text-xs text-gray-500">Consumo</div>
              <div className="font-mono text-sm font-medium">{v.fuelType === "Eléctrico" ? `${formatDecimal(v.consumption)} kWh` : `${formatDecimal(v.consumption)} L`}</div>
            </div>
          </div>
        </div>
      ))}

      <p className="text-xs text-gray-400 mt-4 italic">
        Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
      </p>
    </div>
  );
}
