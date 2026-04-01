
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Contacto",
  description: "Contacta con el equipo de Neumaticopedia para reportar errores, sugerencias o consultas.",
  robots: { index: false, follow: true },
};

export default function ContactPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Contacto</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Contacto</h1>

      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <p className="text-gray-600 mb-4">
          ¿Encontraste un dato incorrecto? ¿Quieres sugerir un modelo que falta? ¿Tienes alguna consulta
          sobre los datos de tu vehículo? Nos encantaría escucharte.
        </p>
        <div className="space-y-4">
          <div>
            <h2 className="font-semibold text-gray-900 mb-1">📧 Email</h2>
            <p className="text-gray-600">contacto@neumaticopedia.com</p>
          </div>
          <div>
            <h2 className="font-semibold text-gray-900 mb-1">🐛 Reportar un error</h2>
            <p className="text-gray-600">
              Si encuentras un dato incorrecto (medida de neumático, presión, PCD, etc.), por favor
              indícanos el modelo exacto del vehículo, el dato erróneo y la fuente donde verificaste
              la información correcta. Corregiremos el dato lo antes posible.
            </p>
          </div>
          <div>
            <h2 className="font-semibold text-gray-900 mb-1">💡 Sugerencias</h2>
            <p className="text-gray-600">
              ¿Echas en falta algún modelo o marca? ¿Tienes ideas para mejorar la web? Todas las
              sugerencias son bienvenidas.
            </p>
          </div>
        </div>
      </div>

      <p className="text-sm text-gray-500">
        Tiempo de respuesta habitual: 24-48 horas laborables.
      </p>
    </div>
  );
}

