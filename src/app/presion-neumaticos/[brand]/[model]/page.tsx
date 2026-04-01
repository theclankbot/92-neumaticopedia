import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import GatedLink from "@/components/GatedLink";
import { formatDecimal, getPressureGuide, isPublished } from "@/lib/data";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ brand: string; model: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { brand, model } = await params;
  const guide = getPressureGuide(brand, model);
  if (!guide || !isPublished(guide.model.publishedAt)) return {};

  return {
    title: `Presión de neumáticos ${guide.brand.name} ${guide.model.name}`,
    description: `Presión recomendada de neumáticos para ${guide.brand.name} ${guide.model.name}. Referencias por variante, carga normal y carga completa.`,
    openGraph: {
      images: guide.model.imageUrl ? [{ url: guide.model.imageUrl }] : undefined,
    },
  };
}

export default async function PressureGuidePage({ params }: Props) {
  const { brand, model } = await params;
  const guide = getPressureGuide(brand, model);
  if (!guide || !isPublished(guide.brand.publishedAt) || !isPublished(guide.model.publishedAt)) notFound();

  const { brand: brandData, model: modelData, generations } = guide;
  const firstVariant = generations[0]?.variants[0];
  const variantCount = generations.reduce((count, generation) => count + generation.variants.length, 0);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6 flex flex-wrap gap-1">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-1">›</span>
        <Link href="/presion-neumaticos" className="hover:text-blue-600">Presión</Link>
        <span className="mx-1">›</span>
        <GatedLink href={`/${brandData.slug}`} published={isPublished(brandData.publishedAt)} publishedClassName="hover:text-blue-600">
          {brandData.name}
        </GatedLink>
        <span className="mx-1">›</span>
        <span className="text-gray-900">{modelData.name}</span>
      </nav>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px] mb-8">
        <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8">
          <div className="inline-flex rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700 mb-4">
            Guía de presión por modelo
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
            Presión de neumáticos {brandData.name} {modelData.name}
          </h1>
          <p className="text-gray-600 leading-relaxed mb-5">
            Referencias para {variantCount} variantes del {brandData.name} {modelData.name}. Mostramos presiones delanteras y traseras
            en carga normal y carga completa, junto con el tamaño de neumático y acceso a la ficha técnica detallada de cada versión.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-2xl bg-gray-50 p-4">
              <div className="text-xs uppercase tracking-wide text-gray-500">Años</div>
              <div className="font-semibold text-gray-900 mt-1">{modelData.years}</div>
            </div>
            <div className="rounded-2xl bg-gray-50 p-4">
              <div className="text-xs uppercase tracking-wide text-gray-500">Carrocería</div>
              <div className="font-semibold text-gray-900 mt-1">{modelData.bodyType}</div>
            </div>
            <div className="rounded-2xl bg-gray-50 p-4">
              <div className="text-xs uppercase tracking-wide text-gray-500">Variantes</div>
              <div className="font-semibold text-gray-900 mt-1">{variantCount}</div>
            </div>
            <div className="rounded-2xl bg-gray-50 p-4">
              <div className="text-xs uppercase tracking-wide text-gray-500">Medida base</div>
              <div className="font-semibold text-gray-900 mt-1">{firstVariant?.tireSizeFront || "No disponible"}</div>
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-gray-200 bg-white overflow-hidden">
          {modelData.imageUrl ? (
            <div className="relative aspect-[4/3]">
              <Image
                src={modelData.imageUrl}
                alt={`${brandData.name} ${modelData.name}`}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 100vw, 360px"
              />
            </div>
          ) : (
            <div className="aspect-[4/3] bg-gradient-to-br from-slate-900 to-blue-900" />
          )}
          <div className="p-4">
            <div className="font-semibold text-gray-900">Imagen de referencia del modelo</div>
            <p className="text-sm text-gray-600 mt-1">
              Fuente visual: Wikimedia Commons / Wikipedia{modelData.imageTitle ? ` · ${modelData.imageTitle}` : ""}.
            </p>
          </div>
        </div>
      </div>

      <div className="rounded-3xl border border-gray-200 bg-white p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Tabla de presiones por variante</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 text-left text-gray-500">
                <th className="py-3 pr-4 font-medium">Variante</th>
                <th className="py-3 pr-4 font-medium">Medida</th>
                <th className="py-3 pr-4 font-medium">Del. normal</th>
                <th className="py-3 pr-4 font-medium">Tras. normal</th>
                <th className="py-3 pr-4 font-medium">Del. cargado</th>
                <th className="py-3 pr-4 font-medium">Tras. cargado</th>
                <th className="py-3 font-medium">Ficha</th>
              </tr>
            </thead>
            <tbody>
              {generations.flatMap((generation) =>
                generation.variants.map((variant) => (
                  <tr key={`${generation.slug}-${variant.slug}`} className="border-b border-gray-100 align-top">
                    <td className="py-3 pr-4">
                      <div className="font-medium text-gray-900">{variant.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{generation.yearStart}–{generation.yearEnd}</div>
                    </td>
                    <td className="py-3 pr-4 font-mono text-gray-700">{variant.tireSizeFront}</td>
                    <td className="py-3 pr-4 font-mono text-gray-700">{formatDecimal(variant.tirePressureFrontBar)} bar</td>
                    <td className="py-3 pr-4 font-mono text-gray-700">{formatDecimal(variant.tirePressureRearBar)} bar</td>
                    <td className="py-3 pr-4 font-mono text-gray-700">{formatDecimal(variant.tirePressureFrontLoadedBar)} bar</td>
                    <td className="py-3 pr-4 font-mono text-gray-700">{formatDecimal(variant.tirePressureRearLoadedBar)} bar</td>
                    <td className="py-3">
                      <GatedLink
                        href={variant.detailUrl}
                        published={isPublished(variant.publishedAt)}
                        publishedClassName="text-blue-600 hover:text-blue-800"
                      >
                        Ver ficha
                      </GatedLink>
                    </td>
                  </tr>
                )),
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-gray-200 bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-3">Consejos para comprobar la presión</h2>
          <div className="space-y-3 text-gray-600 leading-relaxed">
            <p>
              La medición debe hacerse con los neumáticos en frío. Si has circulado, espera al menos dos horas o añade la corrección
              recomendada por el fabricante. Usa siempre los valores de la pegatina del marco de puerta o del manual si difieren de esta guía.
            </p>
            <p>
              La carga completa suele requerir más presión, especialmente en el eje trasero. Mantener la presión correcta ayuda a reducir
              desgaste irregular, consumo y riesgo de sobrecalentamiento en autopista.
            </p>
          </div>
        </div>

        <div className="rounded-3xl border border-gray-200 bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-3">Relaciona presión, medida y llanta</h2>
          <div className="space-y-3 text-gray-600 leading-relaxed">
            <p>
              En el {brandData.name} {modelData.name}, la presión recomendada depende de la variante, el tamaño del neumático, la carga y,
              en algunos casos, del tipo de motorización. Por eso mostramos la referencia por versión y no solo una cifra genérica.
            </p>
            <p className="text-xs text-gray-400 italic">
              Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
