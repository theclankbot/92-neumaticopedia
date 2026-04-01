
import { Metadata } from "next";
import Link from "next/link";
import CalculatorClient from "./CalculatorClient";

export const metadata: Metadata = {
  title: "Calculadora de equivalencia de neumáticos",
  description:
    "Calculadora online de equivalencia de neumáticos. Compara medidas, calcula la diferencia de diámetro, error del velocímetro y cambio de altura. Compatible con la normativa ITV española (máx. 3%).",
};

export default function EquivalenciaPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Inicio</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-900">Equivalencia de neumáticos</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        Equivalencia de neumáticos: calculadora online
      </h1>
      <p className="text-gray-600 mb-8 max-w-2xl">
        Compara dos medidas de neumáticos para verificar si son equivalentes según la normativa española
        de la ITV (máximo 3% de desviación en diámetro exterior). Introduce tu medida original y la
        alternativa para ver las diferencias.
      </p>

      <CalculatorClient />

      {/* Info section */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mt-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">¿Cómo leer las medidas de un neumático?</h2>
        <p className="text-sm text-gray-600 leading-relaxed mb-4">
          Las medidas de un neumático se expresan en un formato estándar como <strong>205/55 R16</strong>, donde:
        </p>
        <ul className="text-sm text-gray-600 space-y-2 mb-4">
          <li><strong>205</strong> — Ancho del neumático en milímetros (la anchura de la banda de rodadura)</li>
          <li><strong>55</strong> — Perfil o serie: relación entre la altura del flanco y el ancho, expresada en porcentaje. Un perfil 55 significa que la altura del flanco es el 55% del ancho (205 × 0,55 = 112,75 mm)</li>
          <li><strong>R</strong> — Construcción radial (la más común hoy en día)</li>
          <li><strong>16</strong> — Diámetro interior de la llanta en pulgadas</li>
        </ul>
        <h3 className="text-lg font-bold text-gray-900 mb-3">¿Qué medidas son equivalentes?</h3>
        <p className="text-sm text-gray-600 leading-relaxed mb-4">
          Dos neumáticos son equivalentes cuando su diámetro exterior total es similar. En España, la normativa de la ITV
          permite una desviación máxima del 3% en el diámetro exterior respecto a la medida original homologada.
          Una desviación mayor puede suponer el rechazo en la inspección técnica.
        </p>
        <h3 className="text-lg font-bold text-gray-900 mb-3">¿Cómo se calcula el diámetro exterior?</h3>
        <p className="text-sm text-gray-600 leading-relaxed">
          El diámetro exterior = Diámetro de la llanta (en mm) + 2 × altura del flanco.<br />
          Altura del flanco = Ancho × (Perfil / 100).<br />
          Ejemplo: 205/55 R16 → 16&quot; = 406,4 mm + 2 × (205 × 0,55) = 406,4 + 225,5 = 631,9 mm.
        </p>
        <p className="text-xs text-gray-400 mt-4 italic">
          Esta calculadora es informativa. Consulte siempre con un profesional antes de cambiar las medidas de sus neumáticos.
        </p>
      </div>

      {/* Popular equivalences */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mt-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Equivalencias más buscadas</h2>
        <div className="table-responsive">
          <table className="spec-table">
            <thead>
              <tr>
                <th>Original</th>
                <th>Alternativa</th>
                <th>Diferencia</th>
                <th>ITV</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["195/65 R15", "205/55 R16", "+0,7%", "✅ Compatible"],
                ["205/55 R16", "215/45 R17", "+0,2%", "✅ Compatible"],
                ["225/45 R17", "225/40 R18", "-0,3%", "✅ Compatible"],
                ["195/55 R16", "205/50 R16", "-1,0%", "✅ Compatible"],
                ["215/60 R17", "225/55 R18", "+0,8%", "✅ Compatible"],
                ["185/65 R15", "195/60 R15", "-0,4%", "✅ Compatible"],
                ["205/60 R16", "215/55 R16", "-0,8%", "✅ Compatible"],
                ["235/55 R19", "255/45 R20", "+0,5%", "✅ Compatible"],
              ].map(([orig, alt, diff, itv], i) => (
                <tr key={i}>
                  <td className="font-mono">{orig}</td>
                  <td className="font-mono">{alt}</td>
                  <td className="font-mono">{diff}</td>
                  <td>{itv}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

