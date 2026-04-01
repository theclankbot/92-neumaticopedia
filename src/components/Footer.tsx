import Link from "next/link";
import Logo from "./Logo";
import GatedLink from "./GatedLink";
import { getAllBrands, isPublished } from "@/lib/data";

export default function Footer() {
  const topBrands = getAllBrands().slice(0, 10);

  return (
    <footer className="bg-slate-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <Logo className="h-8 w-auto mb-4 [&_text]:fill-white [&_circle]:stroke-blue-400 [&_line]:stroke-blue-400 [&_circle:last-of-type]:fill-blue-400" />
            <p className="text-sm text-gray-400 mt-3">
              Base de datos de neumáticos, llantas, patrones PCD y presión recomendada por marca, modelo, año y variante.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-3">Marcas populares</h3>
            <ul className="space-y-1.5 text-sm">
              {topBrands.slice(0, 5).map((brand) => (
                <li key={brand.slug}>
                  <GatedLink
                    href={`/${brand.slug}`}
                    published={isPublished(brand.publishedAt)}
                    publishedClassName="hover:text-white transition-colors"
                    unpublishedClassName="text-gray-500"
                  >
                    {brand.name}
                  </GatedLink>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-3">Más marcas</h3>
            <ul className="space-y-1.5 text-sm">
              {topBrands.slice(5).map((brand) => (
                <li key={brand.slug}>
                  <GatedLink
                    href={`/${brand.slug}`}
                    published={isPublished(brand.publishedAt)}
                    publishedClassName="hover:text-white transition-colors"
                    unpublishedClassName="text-gray-500"
                  >
                    {brand.name}
                  </GatedLink>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-3">Herramientas</h3>
            <ul className="space-y-1.5 text-sm">
              <li><Link href="/equivalencia-neumaticos" className="hover:text-white transition-colors">Calculadora de equivalencias</Link></li>
              <li><Link href="/neumaticos" className="hover:text-white transition-colors">Medidas de neumáticos</Link></li>
              <li><Link href="/pcd" className="hover:text-white transition-colors">Patrones PCD</Link></li>
              <li><Link href="/presion-neumaticos" className="hover:text-white transition-colors">Guías de presión</Link></li>
            </ul>
            <h3 className="font-semibold text-white mb-3 mt-6">Legal</h3>
            <ul className="space-y-1.5 text-sm">
              <li><Link href="/sobre-nosotros" className="hover:text-white transition-colors">Sobre nosotros</Link></li>
              <li><Link href="/fuentes-de-datos" className="hover:text-white transition-colors">Fuentes de datos</Link></li>
              <li><Link href="/contacto" className="hover:text-white transition-colors">Contacto</Link></li>
              <li><Link href="/privacidad" className="hover:text-white transition-colors">Privacidad</Link></li>
              <li><Link href="/terminos" className="hover:text-white transition-colors">Términos</Link></li>
              <li><Link href="/cookies" className="hover:text-white transition-colors">Cookies</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-700 mt-8 pt-6">
          <p className="text-xs text-gray-500 mb-2">
            Los datos de medidas y especificaciones son informativos. Consulte siempre con el fabricante o un profesional antes de realizar cualquier cambio en los neumáticos o llantas de su vehículo.
          </p>
          <p className="text-xs text-gray-500 mb-4">
            Algunos enlaces de esta web son de afiliados. Si compras a través de ellos, podemos recibir una comisión sin coste adicional para ti.
          </p>
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} Neumaticopedia.com — Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
