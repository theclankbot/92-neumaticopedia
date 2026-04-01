import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getBrand, isPublished } from "@/lib/data";
import GatedLink from "@/components/GatedLink";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ brand: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { brand: slug } = await params;
  const brand = getBrand(slug);
  if (!brand || !isPublished(brand.publishedAt)) return {};

  return {
    title: `${brand.name}: medidas de neumáticos y llantas por modelo`,
    description: `Consulta las medidas de neumáticos, presión, PCD y llantas para ${brand.models.length} modelos de ${brand.name}.`,
  };
}

const SEGMENT_ORDER = ["Mini", "Utilitario", "Compacto", "Medio", "Grande", "Premium", "Comercial", "Deportivo"];

export default async function BrandPage({ params }: Props) {
  const { brand: slug } = await params;
  const brand = getBrand(slug);
  if (!brand || !isPublished(brand.publishedAt)) notFound();

  const modelsBySegment = brand.models.reduce<Record<string, typeof brand.models>>((acc, model) => {
    const segment = model.segment || "Otro";
    if (!acc[segment]) acc[segment] = [];
    acc[segment].push(model);
    return acc;
  }, {});

  const tireSizes: Record<string, number> = {};
  const pcdPatterns: Record<string, number> = {};

  for (const model of brand.models) {
    for (const generation of model.generations) {
      for (const variant of generation.variants) {
        tireSizes[variant.tireSizeFront] = (tireSizes[variant.tireSizeFront] || 0) + 1;
        pcdPatterns[variant.pcd] = (pcdPatterns[variant.pcd] || 0) + 1;
      }
    }
  }

  const topTireSizes = Object.entries(tireSizes).sort((a, b) => b[1] - a[1]).slice(0, 6);
  const topPCDs = Object.entries(pcdPatterns).sort((a, b) => b[1] - a[1]).slice(0, 4);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <Link href="/marcas" className="hover:text-blue-600">Marcas</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">{brand.name}</span>
      </nav>

      <div className="rounded-3xl border border-gray-200 bg-white p-6 md:p-8 mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">Neumáticos y medidas de {brand.name}</h1>
        <p className="text-gray-600 leading-relaxed max-w-4xl mb-5">{brand.description}</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">País</div><div className="font-semibold text-gray-900 mt-1">{brand.country}</div></div>
          <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Fundación</div><div className="font-semibold text-gray-900 mt-1">{brand.founded}</div></div>
          <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Sede</div><div className="font-semibold text-gray-900 mt-1">{brand.hq}</div></div>
          <div className="rounded-2xl bg-gray-50 p-4"><div className="text-gray-500">Modelos</div><div className="font-semibold text-gray-900 mt-1">{brand.models.length}</div></div>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 mb-8">
        <div className="rounded-3xl border border-gray-200 bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Medidas más frecuentes</h2>
          <div className="space-y-3">
            {topTireSizes.map(([size, count]) => (
              <div key={size} className="flex items-center justify-between rounded-2xl bg-blue-50 px-4 py-3">
                <span className="font-mono font-semibold text-blue-700">{size}</span>
                <span className="text-sm text-gray-600">{count} variantes</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl border border-gray-200 bg-white p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Patrones PCD más comunes</h2>
          <div className="space-y-3">
            {topPCDs.map(([pcd, count]) => (
              <div key={pcd} className="flex items-center justify-between rounded-2xl bg-emerald-50 px-4 py-3">
                <span className="font-mono font-semibold text-emerald-700">{pcd}</span>
                <span className="text-sm text-gray-600">{count} variantes</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {SEGMENT_ORDER.filter((segment) => modelsBySegment[segment]).map((segment) => (
        <section key={segment} className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{segment}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            {modelsBySegment[segment].map((model) => {
              const firstVariant = model.generations[0]?.variants[0];
              const published = isPublished(model.publishedAt);
              return (
                <GatedLink
                  key={model.slug}
                  href={`/${brand.slug}/${model.slug}`}
                  published={published}
                  className="block h-full"
                  publishedClassName="group"
                >
                  <article className={`h-full overflow-hidden rounded-3xl border transition-all ${published ? "border-gray-200 bg-white hover:border-blue-300 hover:shadow-md" : "border-gray-100 bg-gray-50"}`}>
                    <div className="relative aspect-[16/10] bg-gradient-to-br from-slate-200 to-slate-100">
                      {model.imageUrl ? (
                        <Image
                          src={model.imageUrl}
                          alt={`${brand.name} ${model.name}`}
                          fill
                          className={`object-cover ${published ? "group-hover:scale-[1.02]" : "opacity-75"} transition-transform`}
                          sizes="(max-width: 1280px) 50vw, 33vw"
                        />
                      ) : null}
                    </div>
                    <div className="p-5">
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div>
                          <h3 className={`text-lg font-semibold ${published ? "text-gray-900" : "text-gray-500"}`}>{model.name}</h3>
                          <p className="text-sm text-gray-600 mt-1">{model.bodyType} • {model.years}</p>
                        </div>
                        {model.current ? <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-700">Actual</span> : null}
                      </div>
                      {firstVariant ? (
                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div className="rounded-2xl bg-gray-50 p-3">
                            <div className="text-xs uppercase tracking-wide text-gray-500">Neumático base</div>
                            <div className="font-mono font-semibold text-gray-900 mt-1">{firstVariant.tireSizeFront}</div>
                          </div>
                          <div className="rounded-2xl bg-gray-50 p-3">
                            <div className="text-xs uppercase tracking-wide text-gray-500">PCD</div>
                            <div className="font-mono font-semibold text-gray-900 mt-1">{firstVariant.pcd}</div>
                          </div>
                        </div>
                      ) : null}
                    </div>
                  </article>
                </GatedLink>
              );
            })}
          </div>
        </section>
      ))}

      <div className="rounded-3xl border border-gray-200 bg-white p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-3">Cómo usar esta guía de {brand.name}</h2>
        <div className="space-y-3 text-gray-600 leading-relaxed">
          <p>
            Cada modelo enlaza a una ficha donde reunimos sus generaciones, variantes, medidas OEM, guías de presión y datos de llanta.
            El objetivo es resolver tanto búsquedas por vehículo como consultas inversas de compatibilidad.
          </p>
          <p>
            Aunque el PCD y la medida del neumático son dos referencias clave, una sustitución correcta también depende del diámetro de buje,
            offset, índice de carga, velocidad y homologación. Verifica siempre la documentación oficial antes de montar otra combinación.
          </p>
          <p className="text-xs text-gray-400 italic">
            Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo.
          </p>
        </div>
      </div>
    </div>
  );
}
