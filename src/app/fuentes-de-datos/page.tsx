import type { Metadata } from "next";
import Link from "next/link";
import { getSourceMetadata } from "@/lib/data";

export const metadata: Metadata = {
  title: "Fuentes de datos: de dónde proviene nuestra información",
  description:
    "Fuentes, metodología y fechas de actualización de los datos utilizados en Neumaticopedia.",
};

export default function DataSourcesPage() {
  const sourceMetadata = getSourceMetadata();
  const wheelSizeBrands = Object.values(sourceMetadata.wheelSize);
  const nhtsaBrands = Object.values(sourceMetadata.nhtsa);
  const wheelSizeUniverse = wheelSizeBrands.reduce((total, brand) => total + brand.modelCount, 0);
  const nhtsaUniverse = nhtsaBrands.reduce((total, brand) => total + brand.count, 0);

  const sources = [
    {
      name: "wheel-size.com",
      url: "https://www.wheel-size.com/",
      description:
        "Referencia principal para la cobertura de marcas y modelos y para la verificación de patrones PCD, medidas OEM y llantas compatibles.",
      items: [
        `Cobertura observada: ${wheelSizeUniverse.toLocaleString("es-ES")} modelos distribuidos entre ${wheelSizeBrands.length} marcas rastreadas`,
        "Datos utilizados: listados de modelos por marca, estructura del universo de vehículos y comprobación de fitment",
        `Última captura de metadatos: ${sourceMetadata.generatedAt}`,
      ],
      license: "Datos públicos consultados para referencia técnica",
    },
    {
      name: "NHTSA vPIC API",
      url: "https://vpic.nhtsa.dot.gov/api/",
      description:
        "API pública de la National Highway Traffic Safety Administration utilizada para contrastar listados de modelos por fabricante y ampliar cobertura.",
      items: [
        `Cobertura acumulada de la API: ${nhtsaUniverse.toLocaleString("es-ES")} modelos reportados entre ${nhtsaBrands.length} marcas consultadas`,
        "Datos utilizados: nombres de modelos por make, normalización y contraste con la base principal",
        `Última consulta agregada: ${sourceMetadata.generatedAt}`,
      ],
      license: "Dominio público (gobierno de EE.UU.)",
    },
    {
      name: "Wikipedia / Wikimedia Commons",
      url: "https://commons.wikimedia.org/",
      description:
        "Enriquecimiento visual de páginas de modelo mediante imágenes libres y páginas de referencia de Wikipedia.",
      items: [
        "Datos utilizados: imágenes de modelos, título de la página de referencia y atribución a Wikimedia Commons / Wikipedia",
        `API consultada: ${sourceMetadata.wikipedia.api}`,
        `Última actualización de imágenes: ${sourceMetadata.wikipedia.fetchedAt}`,
      ],
      license: sourceMetadata.wikipedia.license,
    },
    {
      name: "Normativa ITV y documentación de fabricante",
      url: "https://www.mitma.gob.es/",
      description:
        "Marco de validación editorial para equivalencias de neumáticos, seguridad y comprobaciones antes de sustituir neumáticos o llantas.",
      items: [
        "Criterio aplicado en la calculadora: control de desviación de diámetro exterior",
        "Avisos legales y recomendaciones: verificar siempre manual del vehículo, pegatina del marco de puerta y homologación",
        "Uso: soporte editorial y validación de contenidos, no extracción automatizada masiva",
      ],
      license: "Legislación y documentación pública",
    },
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Fuentes de datos</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-4">Fuentes de datos</h1>
      <p className="text-gray-600 max-w-3xl leading-relaxed mb-8">
        La confianza del proyecto depende de documentar qué fuente aporta cada dato. En esta página detallamos el origen de la cobertura de marcas y modelos,
        la verificación cruzada de listados y el origen de las imágenes que aparecen en las fichas de vehículo.
      </p>

      <div className="space-y-6">
        {sources.map((source) => (
          <section key={source.name} className="rounded-3xl border border-gray-200 bg-white p-6">
            <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
              <div>
                <h2 className="text-xl font-bold text-gray-900">{source.name}</h2>
                <p className="text-sm text-gray-600 mt-1">{source.description}</p>
              </div>
              <a href={source.url} target="_blank" rel="noopener noreferrer" className="text-sm font-semibold text-blue-600 hover:text-blue-800">
                Visitar fuente ↗
              </a>
            </div>
            <ul className="space-y-2 text-sm text-gray-700">
              {source.items.map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="text-blue-500">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
            <div className="mt-4 text-xs text-gray-500">Licencia / condiciones: {source.license}</div>
          </section>
        ))}
      </div>

      <section className="rounded-3xl border border-blue-200 bg-blue-50 p-6 mt-8">
        <h2 className="text-xl font-bold text-blue-900 mb-3">Metodología de cruce y control</h2>
        <ol className="space-y-2 text-sm text-blue-900/90 list-decimal list-inside">
          <li>Partimos del universo de modelos detectado en wheel-size.com por marca.</li>
          <li>Contrastamos ese universo con listados por fabricante de la API pública NHTSA vPIC.</li>
          <li>Generamos fichas estructuradas con neumáticos, PCD, presión y dimensiones por variante.</li>
          <li>Enriquecemos las páginas de modelo con imagen de referencia obtenida desde Wikipedia / Wikimedia Commons.</li>
          <li>Cuando un dato no está publicado todavía, la interfaz lo muestra como “Próximamente” para evitar enlazar a páginas incompletas.</li>
        </ol>
      </section>

      <section className="rounded-3xl border border-gray-200 bg-white p-6 mt-8">
        <h2 className="text-xl font-bold text-gray-900 mb-3">Actualización más reciente</h2>
        <p className="text-gray-600 text-sm leading-relaxed">
          La última regeneración de los metadatos de fuentes, listados cruzados e imágenes se realizó el {sourceMetadata.generatedAt}.
          Los datos de presión, fitment y compatibilidad deben tomarse como referencia informativa y verificarse siempre con la documentación oficial del vehículo.
        </p>
      </section>
    </div>
  );
}
