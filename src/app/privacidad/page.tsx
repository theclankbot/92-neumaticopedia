
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Política de privacidad",
  description: "Política de privacidad de Neumaticopedia. Información sobre el tratamiento de datos personales conforme al RGPD.",
  robots: { index: false, follow: true },
};

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Privacidad</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Política de privacidad</h1>
      <p className="text-sm text-gray-500 mb-6">Última actualización: 1 de abril de 2026</p>

      <div className="prose prose-gray max-w-none prose-sm">
        <h2>1. Responsable del tratamiento</h2>
        <p>El responsable del tratamiento de los datos personales recogidos a través de neumaticopedia.com es su titular. Para cualquier consulta relacionada con la privacidad, puede contactar en: contacto@neumaticopedia.com</p>

        <h2>2. Datos que recopilamos</h2>
        <p>Neumaticopedia recopila los siguientes tipos de datos:</p>
        <ul>
          <li><strong>Datos de navegación:</strong> Dirección IP anonimizada, tipo de navegador, sistema operativo, páginas visitadas, tiempo de permanencia. Estos datos se recopilan a través de Vercel Analytics de forma anónima.</li>
          <li><strong>Cookies técnicas:</strong> Necesarias para el funcionamiento del sitio web. No contienen datos personales identificables.</li>
          <li><strong>Datos de contacto:</strong> Si nos envía un correo electrónico, conservamos su dirección de email y el contenido del mensaje para poder responderle.</li>
        </ul>

        <h2>3. Finalidad del tratamiento</h2>
        <ul>
          <li>Proporcionar el servicio de consulta de datos de neumáticos y vehículos</li>
          <li>Analizar el uso del sitio web para mejorar su contenido y funcionalidad</li>
          <li>Responder a consultas recibidas por email</li>
        </ul>

        <h2>4. Base jurídica</h2>
        <p>El tratamiento de datos se basa en:</p>
        <ul>
          <li>El interés legítimo del responsable en ofrecer y mejorar el servicio (Art. 6.1.f RGPD)</li>
          <li>El consentimiento del usuario para cookies no esenciales (Art. 6.1.a RGPD)</li>
        </ul>

        <h2>5. Conservación de datos</h2>
        <p>Los datos de navegación se conservan de forma anonimizada. Los datos de contacto se conservan durante el tiempo necesario para atender la consulta y, en todo caso, no más de 12 meses desde la última comunicación.</p>

        <h2>6. Derechos del usuario</h2>
        <p>De acuerdo con el RGPD, usted tiene derecho a:</p>
        <ul>
          <li>Acceder a sus datos personales</li>
          <li>Rectificar datos inexactos</li>
          <li>Solicitar la supresión de sus datos</li>
          <li>Oponerse al tratamiento</li>
          <li>Solicitar la portabilidad de sus datos</li>
          <li>Presentar una reclamación ante la Agencia Española de Protección de Datos (AEPD)</li>
        </ul>
        <p>Para ejercer estos derechos, escriba a: contacto@neumaticopedia.com</p>

        <h2>7. Enlaces de afiliados</h2>
        <p>Neumaticopedia puede incluir enlaces a tiendas de neumáticos y otros servicios de terceros a través de programas de afiliación. Cuando hace clic en estos enlaces y realiza una compra, podemos recibir una comisión sin coste adicional para usted. Estos terceros tienen sus propias políticas de privacidad independientes.</p>

        <h2>8. Servicios de terceros</h2>
        <ul>
          <li><strong>Vercel Analytics:</strong> Servicio de análisis web que utiliza datos anonimizados. <a href="https://vercel.com/docs/analytics/privacy-policy" className="text-blue-600" target="_blank" rel="noopener noreferrer">Política de privacidad de Vercel</a></li>
        </ul>

        <h2>9. Cambios en esta política</h2>
        <p>Nos reservamos el derecho de actualizar esta política de privacidad. Cualquier cambio será publicado en esta página con la fecha de actualización correspondiente.</p>
      </div>
    </div>
  );
}

