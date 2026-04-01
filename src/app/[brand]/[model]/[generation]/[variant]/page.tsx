
import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import GatedLink from "@/components/GatedLink";
import { getBrand, isPublished, formatNumber, formatDecimal } from "@/lib/data";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ brand: string; model: string; generation: string; variant: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { brand: bSlug, model: mSlug, generation: gSlug, variant: vSlug } = await params;
  const brand = getBrand(bSlug);
  if (!brand) return {};
  const model = brand.models.find((m) => m.slug === mSlug);
  const gen = model?.generations.find((g) => g.slug === gSlug);
  const variant = gen?.variants.find((v) => v.slug === vSlug);
  if (!variant || !isPublished(variant.publishedAt)) return {};
  return {
    title: `${brand.name} ${model!.name} ${variant.name}: neumáticos ${variant.tireSizeFront}, ficha técnica completa`,
    description: `Ficha técnica del ${brand.name} ${model!.name} ${variant.name}. Neumáticos ${variant.tireSizeFront}, PCD ${variant.pcd}, presión ${formatDecimal(variant.tirePressureFrontBar)} bar. Motor ${variant.displacement ? formatNumber(variant.displacement) + " cc" : "eléctrico"}, ${variant.powerHp} CV.`,
  };
}

function SpecSection({ title, icon, children }: { title: string; icon: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
      <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <span>{icon}</span> {title}
      </h2>
      {children}
    </div>
  );
}

function SpecRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between py-2 border-b border-gray-100 last:border-0">
      <span className="text-gray-600 text-sm">{label}</span>
      <span className="text-gray-900 text-sm font-mono font-medium text-right">{value || "No disponible"}</span>
    </div>
  );
}

export default async function VariantPage({ params }: Props) {
  const { brand: bSlug, model: mSlug, generation: gSlug, variant: vSlug } = await params;
  const brand = getBrand(bSlug);
  if (!brand || !isPublished(brand.publishedAt)) notFound();
  const model = brand.models.find((m) => m.slug === mSlug);
  if (!model || !isPublished(model.publishedAt)) notFound();
  const gen = model.generations.find((g) => g.slug === gSlug);
  if (!gen || !isPublished(gen.publishedAt)) notFound();
  const variant = gen.variants.find((v) => v.slug === vSlug);
  if (!variant || !isPublished(variant.publishedAt)) notFound();

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-6 flex flex-wrap gap-1">
        <Link href="/" className="hover:text-blue-600">Inicio</Link><span className="mx-1">›</span>
        <GatedLink href={`/${brand.slug}`} published={isPublished(brand.publishedAt)} publishedClassName="hover:text-blue-600">{brand.name}</GatedLink><span className="mx-1">›</span>
        <GatedLink href={`/${brand.slug}/${model.slug}`} published={isPublished(model.publishedAt)} publishedClassName="hover:text-blue-600">{model.name}</GatedLink><span className="mx-1">›</span>
        <GatedLink href={`/${brand.slug}/${model.slug}/${gen.slug}`} published={isPublished(gen.publishedAt)} publishedClassName="hover:text-blue-600">{gen.yearStart}–{gen.yearEnd}</GatedLink><span className="mx-1">›</span>
        <span className="text-gray-900">{variant.name}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        {brand.name} {model.name} {variant.name}
      </h1>
      <div className="flex flex-wrap gap-2 text-sm mb-8">
        <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full">{variant.fuelType}</span>
        <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">{variant.powerHp} CV</span>
        <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">{variant.transmission}</span>
        <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">{variant.driveType}</span>
        <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full">{gen.yearStart}–{gen.yearEnd}</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left column */}
        <div>
          {/* Tire specs */}
          <SpecSection title="Neumáticos" icon="🛞">
            <SpecRow label="Medida delantera" value={variant.tireSizeFront} />
            <SpecRow label="Medida trasera" value={variant.tireSizeRear || variant.tireSizeFront} />
            <SpecRow label="Llantas" value={variant.rimSize} />
          </SpecSection>

          {/* Tire pressure */}
          <SpecSection title="Presión de neumáticos" icon="🔧">
            <SpecRow label="Delantero (carga normal)" value={`${formatDecimal(variant.tirePressureFrontBar)} bar`} />
            <SpecRow label="Trasero (carga normal)" value={`${formatDecimal(variant.tirePressureRearBar)} bar`} />
            <SpecRow label="Delantero (carga completa)" value={`${formatDecimal(variant.tirePressureFrontLoadedBar)} bar`} />
            <SpecRow label="Trasero (carga completa)" value={`${formatDecimal(variant.tirePressureRearLoadedBar)} bar`} />
          </SpecSection>

          {/* Wheel specs */}
          <SpecSection title="Especificaciones de llanta" icon="⚙️">
            <SpecRow label="PCD (patrón de anclaje)" value={variant.pcd} />
            <SpecRow label="Diámetro del buje" value={`${variant.centerBore} mm`} />
            <SpecRow label="Offset (ET)" value={`ET${variant.offsetMin} – ET${variant.offsetMax}`} />
            <SpecRow label="Par de apriete" value={`${variant.wheelTorqueNm} Nm`} />
            <SpecRow label="Rosca" value={variant.threadSize} />
            <SpecRow label="Tipo de fijación" value={variant.boltType} />
          </SpecSection>
        </div>

        {/* Right column */}
        <div>
          {/* Engine */}
          <SpecSection title="Motor y rendimiento" icon="🏎️">
            <SpecRow label="Código motor" value={variant.engineCode || "No disponible"} />
            <SpecRow label="Cilindrada" value={variant.displacement ? `${formatNumber(variant.displacement)} cc` : "N/A (eléctrico)"} />
            <SpecRow label="Combustible" value={variant.fuelType} />
            <SpecRow label="Potencia" value={`${variant.powerHp} CV (${variant.powerKw} kW)`} />
            <SpecRow label="Par motor" value={`${variant.torqueNm} Nm`} />
            <SpecRow label="Transmisión" value={variant.transmission} />
            <SpecRow label="Tracción" value={variant.driveType} />
            <SpecRow label="Velocidad máxima" value={`${variant.topSpeed} km/h`} />
            <SpecRow label="0-100 km/h" value={`${formatDecimal(variant.acceleration0100)} s`} />
          </SpecSection>

          {/* Dimensions */}
          <SpecSection title="Dimensiones y peso" icon="📐">
            <SpecRow label="Largo" value={`${formatNumber(variant.lengthMm)} mm`} />
            <SpecRow label="Ancho" value={`${formatNumber(variant.widthMm)} mm`} />
            <SpecRow label="Alto" value={`${formatNumber(variant.heightMm)} mm`} />
            <SpecRow label="Batalla" value={`${formatNumber(variant.wheelbaseMm)} mm`} />
            <SpecRow label="Peso en vacío" value={`${formatNumber(variant.weightKg)} kg`} />
            <SpecRow label="PMA (peso máximo)" value={`${formatNumber(variant.grossWeightKg)} kg`} />
            <SpecRow label="Maletero" value={`${formatNumber(variant.trunkCapacityL)} litros`} />
          </SpecSection>

          {/* Consumption */}
          <SpecSection title="Consumo y emisiones" icon="⛽">
            <SpecRow label="Depósito" value={variant.fuelTankL > 0 ? `${variant.fuelTankL} litros` : "N/A (eléctrico)"} />
            <SpecRow label="Consumo combinado" value={variant.fuelType === "Eléctrico" ? `${formatDecimal(variant.consumption)} kWh/100km` : `${formatDecimal(variant.consumption)} L/100km`} />
            <SpecRow label="Emisiones CO₂" value={variant.co2 > 0 ? `${variant.co2} g/km` : "0 g/km"} />
          </SpecSection>
        </div>
      </div>

      {/* SEO text */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mt-4">
        <h2 className="text-lg font-bold text-gray-900 mb-3">
          Neumáticos del {brand.name} {model.name} {variant.name}
        </h2>
        <p className="text-sm text-gray-600 leading-relaxed mb-3">
          El {brand.name} {model.name} {variant.name} ({gen.yearStart}–{gen.yearEnd}) es un {model.bodyType.toLowerCase()} equipado con
          un motor {variant.fuelType === "Eléctrico" ? "eléctrico" : `de ${formatNumber(variant.displacement)} cc`} que desarrolla{" "}
          {variant.powerHp} CV y {variant.torqueNm} Nm de par. Utiliza neumáticos de medida {variant.tireSizeFront} montados
          sobre llantas {variant.rimSize} con un patrón de anclaje PCD {variant.pcd}.
        </p>
        <p className="text-sm text-gray-600 leading-relaxed mb-3">
          La presión de neumáticos recomendada es de {formatDecimal(variant.tirePressureFrontBar)} bar en el eje delantero
          y {formatDecimal(variant.tirePressureRearBar)} bar en el trasero en condiciones de carga normal.
          Con carga completa, se recomienda aumentar a {formatDecimal(variant.tirePressureFrontLoadedBar)} bar (delantero)
          y {formatDecimal(variant.tirePressureRearLoadedBar)} bar (trasero).
        </p>
        <p className="text-sm text-gray-600 leading-relaxed">
          Al cambiar las llantas, asegúrese de utilizar un diámetro de buje de {variant.centerBore} mm,
          un offset entre ET{variant.offsetMin} y ET{variant.offsetMax}, y aplicar un par de apriete de{" "}
          {variant.wheelTorqueNm} Nm a los {variant.boltType === "Tornillo" ? "tornillos" : "tuercas"} ({variant.threadSize}).
        </p>
        <p className="text-xs text-gray-400 mt-4 italic">
          Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
        </p>
      </div>
    </div>
  );
}
