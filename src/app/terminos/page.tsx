
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Términos de servicio",
  description: "Términos y condiciones de uso de Neumaticopedia.",
  robots: { index: false, follow: true },
};

export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Términos</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Términos de servicio</h1>
      <p className="text-sm text-gray-500 mb-6">Última actualización: 1 de abril de 2026</p>

      <div className="prose prose-gray max-w-none prose-sm">
        <h2>1. Objeto</h2>
        <p>Los presentes términos regulan el acceso y uso del sitio web neumaticopedia.com (en adelante, &quot;el Sitio&quot;), una base de datos de información técnica de vehículos, neumáticos y llantas.</p>

        <h2>2. Naturaleza informativa</h2>
        <p><strong>Toda la información publicada en el Sitio tiene carácter exclusivamente informativo y orientativo.</strong> Los datos de medidas, especificaciones técnicas, presión de neumáticos y equivalencias se ofrecen como referencia general y no sustituyen:</p>
        <ul>
          <li>La consulta del manual del propietario del vehículo</li>
          <li>El asesoramiento de un profesional cualificado del sector del neumático y la automoción</li>
          <li>La información oficial del fabricante del vehículo</li>
          <li>Las verificaciones de la Inspección Técnica de Vehículos (ITV)</li>
        </ul>

        <h2>3. Exoneración de responsabilidad</h2>
        <p>El titular del Sitio no se responsabiliza de:</p>
        <ul>
          <li>Posibles errores o inexactitudes en los datos publicados</li>
          <li>Daños derivados del uso de la información sin verificación profesional</li>
          <li>La disponibilidad o exactitud de los productos o servicios de terceros enlazados desde el Sitio</li>
          <li>Cambios en las especificaciones realizados por los fabricantes con posterioridad a la publicación de los datos</li>
        </ul>

        <h2>4. Propiedad intelectual</h2>
        <p>La estructura, diseño, código fuente y textos originales del Sitio son propiedad de su titular. Los datos técnicos de vehículos provienen de fuentes públicas detalladas en nuestra página de <Link href="/fuentes-de-datos" className="text-blue-600">fuentes de datos</Link>. Las marcas y nombres de modelos son propiedad de sus respectivos titulares.</p>

        <h2>5. Enlaces de afiliados</h2>
        <p>El Sitio puede contener enlaces a tiendas y servicios de terceros a través de programas de afiliación. Estos enlaces se identifican como tal cuando es técnicamente posible. Al acceder a sitios de terceros, se aplican sus propios términos y condiciones.</p>

        <h2>6. Uso aceptable</h2>
        <p>El usuario se compromete a utilizar el Sitio de forma lícita y conforme a estos términos. Queda prohibida la reproducción masiva o automatizada del contenido sin autorización expresa.</p>

        <h2>7. Legislación aplicable</h2>
        <p>Estos términos se rigen por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales de la ciudad de Barcelona, salvo que la normativa de consumo establezca otra cosa.</p>

        <h2>8. Contacto</h2>
        <p>Para cualquier consulta sobre estos términos: contacto@neumaticopedia.com</p>
      </div>
    </div>
  );
}

