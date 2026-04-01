import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { formatDecimal, formatNumber, getBrand, isPublished } from "@/lib/data";
import GatedLink from "@/components/GatedLink";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ brand: string; model: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { brand: brandSlug, model: modelSlug } = await params;
  const brand = getBrand(brandSlug);
  if (!brand) return {};
  const model = brand.models.find((entry) => entry.slug === modelSlug);
  if (!model || !isPublished(model.publishedAt)) return {};

  const firstVariant = model.generations[0]?.variants[0];
  return {
    title: `${brand.name} ${model.name}: medidas neumáticos, dimensiones y ficha técnica`,
    description: `Ficha del ${brand.name} ${model.name} con neumáticos ${firstVariant?.tireSizeFront || "OEM"}, presión recomendada, PCD y dimensiones del vehículo.`,
    openGraph: {
      images: model.imageUrl ? [{ url: model.imageUrl }] : undefined,
    },
  };
}

export default async function ModelPage({ params }: Props) {
  const { brand: brandSlug, model: modelSlug } = await params;
  const brand = getBrand(brandSlug);
  if (!brand || !isPublished(brand.publishedAt)) notFound();
  const model = brand.models.find((entry) => entry.slug === modelSlug);
  if (!model || !isPublished(model.publishedAt)) notFound();

  const firstGeneration = model.generations[0];
  const firstVariant = firstGeneration?.variants[0];
  const variantCount = model.generations.reduce((count, generation) => count + generation.variants.length, 0);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6 flex flex-wrap gap-1">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-1">›</span>
        <Link href="/marcas" className="hover:text-blue-600">Marcas</Link>
        <span className="mx-1">›</span>
        <GatedLink href={`/${brand.slug}`} published={isPublished(brand.publishedAt)} publishedClassName="hover:text-blue-600">
          {brand.name}
        </GatedLink>
        <span className="mx-1">›</span>
        <span className="text-gray-900">{model.name}</span>
      </nav>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px] mb-8">
        <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8">
          <div className="inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 mb-4">
            Ficha técnica por modelo
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
            {brand.name} {model.name}: neumáticos, medidas y especificaciones
          </h1>
          <p className="text-gray-600 leading-relaxed mb-5">
            Centraliza las generaciones, medidas OEM, presión recomendada, PCD, dimensiones y variantes disponibles del {brand.name} {model.name}.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Carrocería</div><div className="font-semibold text-gray-900 mt-1">{model.bodyType}</div></div>
            <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Segmento</div><div className="font-semibold text-gray-900 mt-1">{model.segment}</div></div>
            <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Años</div><div className="font-semibold text-gray-900 mt-1">{model.years}</div></div>
            <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Variantes</div><div className="font-semibold text-gray-900 mt-1">{variantCount}</div></div>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <GatedLink
              href={`/presion-neumaticos/${brand.slug}/${model.slug}`}
              published={isPublished(model.publishedAt)}
              className="rounded-xl bg-amber-500 px-4 py-2 text-sm font-semibold text-white hover:bg-amber-400"
            >
              Ver guía de presión
            </GatedLink>
            <Link href="/equivalencia-neumaticos" className="rounded-xl border border-gray-200 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50">
              Calcular equivalencias
            </Link>
          </div>
        </div>

        <div className="rounded-3xl border border-gray-200 bg-white overflow-hidden">
          {model.imageUrl ? (
            <div className="relative aspect-[4/3]">
              <Image
                src={model.imageUrl}
                alt={`${brand.name} ${model.name}`}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 100vw, 360px"
              />
            </div>
          ) : (
            <div className="aspect-[4/3] bg-gradient-to-br from-slate-900 to-blue-900" />
          )}
          <div className="p-4">
            <div className="font-semibold text-gray-900">Imagen del modelo</div>
            <p className="text-sm text-gray-600 mt-1">Fuente visual: Wikimedia Commons / Wikipedia.</p>
          </div>
        </div>
      </div>

      {model.generations.map((generation) => (
        <section key={generation.slug} className="mb-10">
          <div className="flex flex-wrap items-end justify-between gap-3 mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{generation.name}</h2>
              <p className="text-gray-600 text-sm mt-1">{generation.yearStart}–{generation.yearEnd} · {generation.variants.length} variantes</p>
            </div>
            <GatedLink
              href={`/${brand.slug}/${model.slug}/${generation.slug}`}
              published={isPublished(generation.publishedAt)}
              publishedClassName="text-sm font-semibold text-blue-600 hover:text-blue-800"
            >
              Ver página de generación
            </GatedLink>
          </div>

          <div className="rounded-3xl border border-gray-200 bg-white overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 text-left text-gray-500">
                    <th className="py-3 px-4 font-medium">Variante</th>
                    <th className="py-3 px-4 font-medium">Neumáticos</th>
                    <th className="py-3 px-4 font-medium">PCD</th>
                    <th className="py-3 px-4 font-medium">Presión</th>
                    <th className="py-3 px-4 font-medium">Motor</th>
                    <th className="py-3 px-4 font-medium">Dimensiones</th>
                    <th className="py-3 px-4 font-medium">Ficha</th>
                  </tr>
                </thead>
                <tbody>
                  {generation.variants.map((variant) => (
                    <tr key={variant.slug} className="border-b border-gray-100 align-top">
                      <td className="py-4 px-4">
                        <div className="font-medium text-gray-900">{variant.name}</div>
                        <div className="text-xs text-gray-500 mt-1">{variant.fuelType} · {variant.transmission}</div>
                      </td>
                      <td className="py-4 px-4 font-mono text-gray-700">{variant.tireSizeFront}</td>
                      <td className="py-4 px-4 font-mono text-gray-700">{variant.pcd}</td>
                      <td className="py-4 px-4 text-gray-700">{formatDecimal(variant.tirePressureFrontBar)} / {formatDecimal(variant.tirePressureRearBar)} bar</td>
                      <td className="py-4 px-4 text-gray-700">{variant.displacement ? `${formatNumber(variant.displacement)} cc` : "Eléctrico"} · {variant.powerHp} CV</td>
                      <td className="py-4 px-4 text-gray-700">{formatNumber(variant.lengthMm)} × {formatNumber(variant.widthMm)} × {formatNumber(variant.heightMm)} mm</td>
                      <td className="py-4 px-4">
                        <GatedLink
                          href={`/${brand.slug}/${model.slug}/${generation.slug}/${variant.slug}`}
                          published={isPublished(variant.publishedAt)}
                          publishedClassName="text-blue-600 hover:text-blue-800"
                        >
                          Ver ficha
                        </GatedLink>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      ))}

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-blue-200 bg-blue-50 p-6">
          <h2 className="text-lg font-bold text-blue-900 mb-2">Neumático de referencia</h2>
          <p className="font-mono text-2xl font-semibold text-blue-900">{firstVariant?.tireSizeFront || "No disponible"}</p>
          <p className="text-sm text-blue-900/80 mt-2">Medida OEM más habitual en la base de datos para este modelo.</p>
        </div>
        <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6">
          <h2 className="text-lg font-bold text-emerald-900 mb-2">PCD más habitual</h2>
          <p className="font-mono text-2xl font-semibold text-emerald-900">{firstVariant?.pcd || "No disponible"}</p>
          <p className="text-sm text-emerald-900/80 mt-2">Acompáñalo siempre del buje y del offset correctos antes de cambiar llantas.</p>
        </div>
        <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="text-lg font-bold text-amber-900 mb-2">Presión de partida</h2>
          <p className="text-2xl font-semibold text-amber-900">
            {firstVariant ? `${formatDecimal(firstVariant.tirePressureFrontBar)} / ${formatDecimal(firstVariant.tirePressureRearBar)} bar` : "No disponible"}
          </p>
          <p className="text-sm text-amber-900/80 mt-2">Consulta la guía específica del modelo para ver presión con carga completa y por variante.</p>
        </div>
      </div>

      <div className="rounded-3xl border border-gray-200 bg-white p-6 mt-8">
        <h2 className="text-xl font-bold text-gray-900 mb-3">Qué incluye esta ficha del {brand.name} {model.name}</h2>
        <div className="space-y-3 text-gray-600 leading-relaxed">
          <p>
            Mostramos la estructura completa del modelo: generaciones, variantes mecánicas, neumáticos OEM, presión recomendada, medidas de llanta,
            diámetro de buje, par de apriete y datos de dimensión del vehículo.
          </p>
          <p>
            Si estás valorando montar una medida alternativa, utiliza también nuestra calculadora de equivalencias y revisa siempre el manual del fabricante,
            la homologación y la normativa ITV antes de efectuar el cambio.
          </p>
          <p className="text-xs text-gray-400 italic">Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.</p>
        </div>
      </div>
    </div>
  );
}
