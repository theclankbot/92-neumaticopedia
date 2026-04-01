
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { CookieConsentBanner } from "@/components/CookieConsent";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "Neumáticos por coche: medidas, presión y equivalencias | Neumaticopedia",
    template: "%s | Neumaticopedia",
  },
  description:
    "Base de datos de neumáticos por marca, modelo y año. Consulta medidas originales, equivalencias, presión recomendada y especificaciones de llantas para tu vehículo.",
  metadataBase: new URL("https://neumaticopedia.com"),
  openGraph: {
    type: "website",
    locale: "es_ES",
    siteName: "Neumaticopedia",
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: "https://neumaticopedia.com",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className={inter.variable}>
      <body className="min-h-screen flex flex-col bg-gray-50 font-sans antialiased">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
        <CookieConsentBanner />
      </body>
    </html>
  );
}
