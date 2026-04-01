'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Analytics } from '@vercel/analytics/next';
import { SpeedInsights } from '@vercel/speed-insights/next';

const CONSENT_KEY = 'neumaticopedia_cookie_consent';

export function CookieConsentBanner() {
  const [show, setShow] = useState(false);
  const [consent, setConsent] = useState<boolean | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(CONSENT_KEY);
    const newShow = stored === null;
    const newConsent = stored !== null ? stored === 'true' : null;
    if (newShow !== show) setShow(newShow);
    if (newConsent !== consent) setConsent(newConsent);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const accept = () => {
    localStorage.setItem(CONSENT_KEY, 'true');
    setConsent(true);
    setShow(false);
  };

  const reject = () => {
    localStorage.setItem(CONSENT_KEY, 'false');
    setConsent(false);
    setShow(false);
  };

  return (
    <>
      {consent === true && (
        <>
          <Analytics />
          <SpeedInsights />
        </>
      )}
      {show && (
        <div
          role="dialog"
          aria-label="Aviso de cookies"
          className="fixed bottom-0 left-0 right-0 z-50 bg-gray-900 text-white p-4 md:p-5 shadow-2xl"
        >
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center gap-4">
            <div className="flex-1 text-sm md:text-base">
              <p className="font-semibold mb-1">🍪 Usamos cookies analíticas</p>
              <p className="text-gray-300 text-sm">
                Utilizamos cookies de análisis (Vercel Analytics) para mejorar el sitio. Puedes aceptar o rechazar su uso. Ver{' '}
                <Link href="/cookies" className="underline text-blue-400 hover:text-blue-300">
                  política de cookies
                </Link>.
              </p>
            </div>
            <div className="flex gap-3 shrink-0">
              <button
                onClick={reject}
                className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Rechazar
              </button>
              <button
                onClick={accept}
                className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors"
              >
                Aceptar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
