# Project Definition: Llantas y Neumáticos

## Concepto
Base de datos exhaustiva de medidas de neumáticos y llantas por marca/modelo/año de coche. El usuario llega buscando qué medida necesita su coche, y le damos eso + toda la info técnica relevante del vehículo.

## Ángulo diferencial
wheel-size.com domina pero su UX es terrible y todo está en inglés. Empezamos en español (España) donde hay menos competencia, con una UX mucho mejor y datos cruzados de múltiples fuentes que nadie más tiene juntos.

## Target
- Idioma: Español (España primero, luego expandible a LATAM)
- País: España (db=es para Semrush)
- Audiencia: cualquier conductor que necesita cambiar neumáticos o llantas

## Dominio
neumaticopedia.com (confirmado disponible vía Spaceship API)

## Modelo de entidades
- Marca (Toyota, BMW, Seat, etc.)
  - Modelo (Corolla, Serie 3, León, etc.)
    - Generación/Año (2020-2024, etc.)
      - Variante/Motor (1.6 TDI, 2.0 TSI, etc.)
        - Medidas OEM (neumáticos originales)
        - Medidas compatibles (alternativas que encajan)

## Datos a cruzar por vehículo (además de llantas/neumáticos)
- Especificaciones técnicas: motor, potencia, par, transmisión
- Dimensiones: largo, ancho, alto, distancia entre ejes
- Peso: en vacío, máximo
- Consumo y emisiones
- Tipo de combustible
- Precio orientativo (nuevo/usado)
- Foto del vehículo
- Presión de neumáticos recomendada
- PCD (patrón de tornillos), offset, diámetro del buje
- Par de apriete de las ruedas

## Monetización
- Afiliación tiendas de neumáticos: Norauto, Feu Vert, Tirerack, Neumaticos.es
- AdSense (tráfico informativo alto)
- Links a comparadores de seguros de coche (cross-sell)

## Seed Keywords para Semrush (db=es)
1. "neumáticos" — broad match cubre todo: medidas, presión, marcas, precios, por modelo...
2. "llantas" — término diferente, gente que busca la llanta no el neumático

Solo 2 seeds. Broad match en Semrush ya saca todas las variaciones.

## Competidores para analizar en Semrush (verificados en SERPs reales)
1. llantasneumaticos.com — wheel-size en español, estructura marca→modelo→specs, nuestro rival directo
2. medidasdecoches.com — #1 para "medidas neumaticos", dominio brutal, tiene fitment data
3. muchoneumatico.com — tiene medidas por marca/modelo, aparece en varias SERPs
4. oponeo.es — tabla presión + calculadora medidas, #1 para "presion neumaticos"
5. presion-de-neumaticos.es — nicho específico de presión por modelo

Nota: michelin.es, norauto.es, feuvert.es rankean pero son marcas/tiendas, no competidores de estructura pSEO

## Fuentes de datos identificadas
1. **wheel-size.com API** — tienen API con free tier (5000 req/día). Marcas, modelos, años, medidas OEM y compatibles, PCD, offset, hub bore. Es la fuente principal.
2. **Teoalida car database** — CSV/Excel con specs técnicos detallados por modelo. Puede complementar.
3. **NHTSA API** (USA) — datos técnicos de vehículos gratuitos, útil como referencia.
4. **Wikipedia/Wikidata** — imágenes y datos básicos de modelos de coche.
5. **Scraping de DGT/ITV** — datos de homologación española si están accesibles.
6. **OpenStreetMap/Nominatim** — para talleres y tiendas cercanas (fase 2).

## Publicación progresiva
- Empezar con las 20 marcas más vendidas en España (Seat, Volkswagen, Renault, Peugeot, Toyota, etc.)
- Dentro de cada marca, todos los modelos actuales (2020-2025)
- Cluster completo: marca + todos sus modelos + todas sus generaciones
- 20-30 páginas/día al inicio

## Notas
- El competidor principal (wheel-size.com) tiene API pública — esto facilita enormemente la obtención de datos
- Multi-idioma en el futuro (en, de, fr) — la estructura debe soportarlo
- Presión de neumáticos es un intent informativo enorme que no todos los competidores cubren bien
