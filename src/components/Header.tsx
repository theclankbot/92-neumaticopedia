"use client";

import Link from "next/link";
import Logo from "./Logo";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/marcas", label: "Marcas" },
  { href: "/neumaticos", label: "Neumáticos" },
  { href: "/pcd", label: "PCD" },
  { href: "/presion-neumaticos", label: "Presión" },
  { href: "/equivalencia-neumaticos", label: "Equivalencias" },
  { href: "/fuentes-de-datos", label: "Datos" },
];

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-14 gap-4">
          <Link href="/" className="shrink-0">
            <Logo className="h-7 w-auto" />
          </Link>

          <nav className="hidden lg:flex items-center gap-6 text-sm font-medium text-gray-700">
            {NAV_LINKS.map((link) => (
              <Link key={link.href} href={link.href} className="hover:text-blue-600 transition-colors">
                {link.label}
              </Link>
            ))}
            <Link href="/sobre-nosotros" className="hover:text-blue-600 transition-colors">
              Sobre nosotros
            </Link>
          </nav>

          <button
            className="lg:hidden p-2 text-gray-600"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Menú"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-gray-200 bg-white">
          <nav className="px-4 py-3 space-y-2">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="block py-2 text-gray-700 hover:text-blue-600"
                onClick={() => setMobileMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <Link href="/sobre-nosotros" className="block py-2 text-gray-700 hover:text-blue-600" onClick={() => setMobileMenuOpen(false)}>Sobre nosotros</Link>
            <Link href="/contacto" className="block py-2 text-gray-700 hover:text-blue-600" onClick={() => setMobileMenuOpen(false)}>Contacto</Link>
          </nav>
        </div>
      )}
    </header>
  );
}
