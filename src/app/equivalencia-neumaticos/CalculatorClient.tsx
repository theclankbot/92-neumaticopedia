
"use client";

import { useState } from "react";

interface TireSize {
  width: number;
  profile: number;
  diameter: number;
}

function parseTireSize(w: string, p: string, d: string): TireSize | null {
  const width = parseInt(w);
  const profile = parseInt(p);
  const diameter = parseInt(d);
  if (isNaN(width) || isNaN(profile) || isNaN(diameter)) return null;
  if (width < 100 || width > 400 || profile < 20 || profile > 90 || diameter < 12 || diameter > 24) return null;
  return { width, profile, diameter };
}

function calcOuterDiameter(tire: TireSize): number {
  const rimMm = tire.diameter * 25.4;
  const sidewall = tire.width * (tire.profile / 100);
  return rimMm + 2 * sidewall;
}

function calcCircumference(diameter: number): number {
  return Math.PI * diameter;
}

export default function CalculatorClient() {
  const [orig, setOrig] = useState({ width: "205", profile: "55", diameter: "16" });
  const [alt, setAlt] = useState({ width: "215", profile: "45", diameter: "17" });

  const origTire = parseTireSize(orig.width, orig.profile, orig.diameter);
  const altTire = parseTireSize(alt.width, alt.profile, alt.diameter);

  const origDiam = origTire ? calcOuterDiameter(origTire) : 0;
  const altDiam = altTire ? calcOuterDiameter(altTire) : 0;

  const diffPercent = origDiam > 0 ? ((altDiam - origDiam) / origDiam) * 100 : 0;
  const speedoError = origDiam > 0 ? ((origDiam - altDiam) / altDiam) * 100 : 0;
  const heightDiff = origDiam > 0 ? (altDiam - origDiam) / 2 : 0;

  const itvOk = Math.abs(diffPercent) <= 3;

  const inputClass = "w-full px-3 py-2 border border-gray-300 rounded-lg text-center font-mono text-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500";

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      {/* Original tire */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Medida original</h2>
        <div className="flex items-center gap-2 mb-4">
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Ancho</label>
            <input type="number" value={orig.width} onChange={(e) => setOrig({ ...orig, width: e.target.value })} className={inputClass} placeholder="205" />
          </div>
          <span className="text-gray-400 font-bold mt-5">/</span>
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Perfil</label>
            <input type="number" value={orig.profile} onChange={(e) => setOrig({ ...orig, profile: e.target.value })} className={inputClass} placeholder="55" />
          </div>
          <span className="text-gray-400 font-bold mt-5">R</span>
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Llanta</label>
            <input type="number" value={orig.diameter} onChange={(e) => setOrig({ ...orig, diameter: e.target.value })} className={inputClass} placeholder="16" />
          </div>
        </div>
        {origTire && (
          <div className="text-sm text-gray-600 space-y-1">
            <div>Diámetro exterior: <span className="font-mono font-medium">{origDiam.toFixed(1).replace(".", ",")} mm</span></div>
            <div>Circunferencia: <span className="font-mono font-medium">{calcCircumference(origDiam).toFixed(1).replace(".", ",")} mm</span></div>
            <div>Altura del flanco: <span className="font-mono font-medium">{(origTire.width * origTire.profile / 100).toFixed(1).replace(".", ",")} mm</span></div>
          </div>
        )}
      </div>

      {/* Alternative tire */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Medida alternativa</h2>
        <div className="flex items-center gap-2 mb-4">
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Ancho</label>
            <input type="number" value={alt.width} onChange={(e) => setAlt({ ...alt, width: e.target.value })} className={inputClass} placeholder="215" />
          </div>
          <span className="text-gray-400 font-bold mt-5">/</span>
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Perfil</label>
            <input type="number" value={alt.profile} onChange={(e) => setAlt({ ...alt, profile: e.target.value })} className={inputClass} placeholder="45" />
          </div>
          <span className="text-gray-400 font-bold mt-5">R</span>
          <div className="flex-1">
            <label className="text-xs text-gray-500 block mb-1">Llanta</label>
            <input type="number" value={alt.diameter} onChange={(e) => setAlt({ ...alt, diameter: e.target.value })} className={inputClass} placeholder="17" />
          </div>
        </div>
        {altTire && (
          <div className="text-sm text-gray-600 space-y-1">
            <div>Diámetro exterior: <span className="font-mono font-medium">{altDiam.toFixed(1).replace(".", ",")} mm</span></div>
            <div>Circunferencia: <span className="font-mono font-medium">{calcCircumference(altDiam).toFixed(1).replace(".", ",")} mm</span></div>
            <div>Altura del flanco: <span className="font-mono font-medium">{(altTire.width * altTire.profile / 100).toFixed(1).replace(".", ",")} mm</span></div>
          </div>
        )}
      </div>

      {/* Results */}
      {origTire && altTire && (
        <div className="md:col-span-2">
          <div className={`rounded-xl border-2 p-6 ${itvOk ? "border-green-300 bg-green-50" : "border-red-300 bg-red-50"}`}>
            <div className="flex items-center gap-3 mb-4">
              <div className={`text-3xl ${itvOk ? "" : ""}`}>{itvOk ? "✅" : "❌"}</div>
              <div>
                <h3 className={`font-bold text-lg ${itvOk ? "text-green-800" : "text-red-800"}`}>
                  {itvOk ? "Compatible según ITV" : "NO compatible según ITV"}
                </h3>
                <p className={`text-sm ${itvOk ? "text-green-700" : "text-red-700"}`}>
                  La diferencia de diámetro es del {Math.abs(diffPercent).toFixed(2).replace(".", ",")}%
                  {itvOk ? " (máximo permitido: 3%)" : " (supera el máximo del 3%)"}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white/60 rounded-lg p-3">
                <div className="text-xs text-gray-500">Diferencia diámetro</div>
                <div className="font-mono font-bold text-lg">
                  {diffPercent > 0 ? "+" : ""}{diffPercent.toFixed(2).replace(".", ",")}%
                </div>
              </div>
              <div className="bg-white/60 rounded-lg p-3">
                <div className="text-xs text-gray-500">Error velocímetro</div>
                <div className="font-mono font-bold text-lg">
                  {speedoError > 0 ? "+" : ""}{speedoError.toFixed(2).replace(".", ",")}%
                </div>
              </div>
              <div className="bg-white/60 rounded-lg p-3">
                <div className="text-xs text-gray-500">Cambio de altura</div>
                <div className="font-mono font-bold text-lg">
                  {heightDiff > 0 ? "+" : ""}{heightDiff.toFixed(1).replace(".", ",")} mm
                </div>
              </div>
              <div className="bg-white/60 rounded-lg p-3">
                <div className="text-xs text-gray-500">A 120 km/h marca</div>
                <div className="font-mono font-bold text-lg">
                  {(120 * (1 + speedoError / 100)).toFixed(1).replace(".", ",")} km/h
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
