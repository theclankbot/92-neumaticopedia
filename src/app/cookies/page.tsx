
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Política de cookies",
  description: "Información sobre las cookies utilizadas en Neumaticopedia conforme a la LSSI.",
  robots: { index: false, follow: true },
};

export default function CookiesPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Cookies</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Política de cookies</h1>
      <p className="text-sm text-gray-500 mb-6">Última actualización: 1 de abril de 2026</p>

      <div className="prose prose-gray max-w-none prose-sm">
        <h2>¿Qué son las cookies?</h2>
        <p>Las cookies son pequeños archivos de texto que los sitios web almacenan en su navegador. Se utilizan para recordar preferencias, mejorar la experiencia de navegación y recopilar estadísticas de uso anónimas.</p>

        <h2>Cookies que utilizamos</h2>

        <h3>Cookies técnicas (necesarias)</h3>
        <p>Estas cookies son estrictamente necesarias para el funcionamiento del sitio web. No requieren consentimiento.</p>
        <div className="table-responsive">
          <table>
            <thead>
              <tr><th>Cookie</th><th>Propósito</th><th>Duración</th></tr>
            </thead>
            <tbody>
              <tr><td>__vercel_live_token</td><td>Verificación de Vercel</td><td>Sesión</td></tr>
            </tbody>
          </table>
        </div>

        <h3>Cookies analíticas</h3>
        <p>Utilizamos Vercel Analytics para comprender cómo los usuarios interactúan con el sitio. Estos datos son anónimos y no permiten identificar a usuarios individuales.</p>
        <div className="table-responsive">
          <table>
            <thead>
              <tr><th>Cookie</th><th>Propósito</th><th>Duración</th></tr>
            </thead>
            <tbody>
              <tr><td>va (Vercel Analytics)</td><td>Análisis de uso anónimo</td><td>Sesión</td></tr>
            </tbody>
          </table>
        </div>

        <h2>¿Cómo gestionar las cookies?</h2>
        <p>Puede configurar su navegador para rechazar cookies o para que le avise cuando un sitio intente establecerlas. Tenga en cuenta que rechazar las cookies técnicas puede afectar al funcionamiento del sitio.</p>
        <ul>
          <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer" className="text-blue-600">Google Chrome</a></li>
          <li><a href="https://support.mozilla.org/es/kb/cookies-informacion-que-los-sitios-web-guardan-en-" target="_blank" rel="noopener noreferrer" className="text-blue-600">Firefox</a></li>
          <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471" target="_blank" rel="noopener noreferrer" className="text-blue-600">Safari</a></li>
          <li><a href="https://support.microsoft.com/es-es/microsoft-edge/eliminar-cookies-en-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener noreferrer" className="text-blue-600">Microsoft Edge</a></li>
        </ul>

        <h2>Base legal</h2>
        <p>Esta política de cookies cumple con la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE) y con el Reglamento General de Protección de Datos (RGPD).</p>

        <h2>Contacto</h2>
        <p>Para cualquier consulta sobre nuestra política de cookies: contacto@neumaticopedia.com</p>
      </div>
    </div>
  );
}

