
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Sobre Neumaticopedia: quiénes somos y nuestra misión",
  description: "Neumaticopedia es la base de datos más completa en español de neumáticos, llantas y especificaciones técnicas de vehículos. Conoce nuestra misión, metodología y equipo.",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Sobre nosotros</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-6">Sobre Neumaticopedia</h1>

      <div className="prose prose-gray max-w-none">
        <h2>Nuestra misión</h2>
        <p>
          Neumaticopedia nace con un objetivo claro: ofrecer a los conductores de habla hispana la base de datos más
          completa y fiable de neumáticos, llantas y especificaciones técnicas de vehículos. Creemos que encontrar
          la medida correcta de neumático para tu coche no debería ser complicado.
        </p>

        <h2>¿Qué encontrarás aquí?</h2>
        <p>Para cada vehículo, ofrecemos:</p>
        <ul>
          <li><strong>Medidas de neumáticos originales (OEM)</strong> — las medidas que monta el vehículo de fábrica</li>
          <li><strong>Especificaciones de llanta</strong> — PCD (patrón de anclaje), offset, diámetro del buje, par de apriete y tipo de fijación</li>
          <li><strong>Presión recomendada</strong> — valores en bar para carga normal y completa, eje delantero y trasero</li>
          <li><strong>Ficha técnica completa</strong> — motor, potencia, dimensiones, peso, consumo y emisiones</li>
          <li><strong>Calculadora de equivalencias</strong> — para verificar si una medida alternativa es compatible según la normativa ITV española</li>
        </ul>

        <h2>Nuestra metodología</h2>
        <p>
          Los datos de Neumaticopedia provienen de fuentes públicas verificadas, incluyendo bases de datos técnicas
          de la industria automotriz, la API pública de NHTSA (National Highway Traffic Safety Administration de EE.UU.),
          datos de Wikipedia/Wikidata y documentación oficial de los fabricantes.
        </p>
        <p>
          Cada dato se cruza con al menos dos fuentes cuando es posible. Los valores de presión de neumáticos,
          medidas y especificaciones de llanta se verifican contra la documentación técnica del vehículo.
          Cuando un dato no puede verificarse con certeza, lo indicamos como &quot;No disponible&quot; en lugar de mostrar
          información potencialmente incorrecta.
        </p>

        <h2>Aviso importante</h2>
        <p>
          Toda la información publicada en Neumaticopedia tiene carácter meramente informativo. Aunque nos esforzamos
          por mantener los datos actualizados y correctos, <strong>siempre recomendamos verificar las medidas y
          especificaciones con el manual del vehículo o un profesional cualificado</strong> antes de realizar
          cualquier cambio en los neumáticos o llantas de su vehículo.
        </p>

        <h2>Contacto</h2>
        <p>
          ¿Encontraste un error en nuestros datos? ¿Tienes una sugerencia? Nos encantaría escucharte.
          Puedes contactarnos a través de nuestra <Link href="/contacto" className="text-blue-600 hover:text-blue-800">página de contacto</Link>.
        </p>
      </div>
    </div>
  );
}

