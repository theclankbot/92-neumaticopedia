# Project Brief: neumaticopedia.com

**Domain:** neumaticopedia.com  
**Status:** Brief Review  
**Date:** 2026-04-01  
**Author:** Strategist (Web Factory)

---

## 1. Executive Summary

**Concept:** neumaticopedia.com is an exhaustive database of tire and wheel sizes organized by car brand, model, generation, and variant. Users search what tire fits their car and get OEM sizes, compatible alternatives, and all cross-referenced technical specifications — from tire pressure and bolt patterns to engine specs and vehicle dimensions.

**Market opportunity:** Analysis of medidasdecoches.com (the #1 Spanish competitor for car dimensions) reveals 26,593 organic keywords generating 43,129 monthly visits from 4.89M total search volume. The site dominates "medidas de coches" (8,100 vol) but barely touches tire/wheel-specific queries. Meanwhile, wheel-size.com dominates globally but has no Spanish presence and terrible UX. This leaves a massive gap for a Spanish-language tire fitment database with superior UX and cross-referenced data.

**Quick win potential:** 10,771 keywords with KD<30 and Vol>100 representing 3.6M total search volume — mostly informational intent (92.5%) which is our sweet spot.

**Monetization:** Tire shop affiliate programs (Norauto, Feu Vert, Neumaticos.es), AdSense on informational pages, car insurance cross-sell.

**Target:** Spanish speakers in Spain (db=es), expandable to LATAM markets later.

**Tech stack:** Next.js App Router, static JSON data files, progressive publication with publishedAt dates, GatedLink component for unpublished pages.

---

## 2. Keyword Analysis

### 2.1 Dataset Overview (medidasdecoches.com organic positions)

| Metric | Value |
|---|---|
| Total keywords ranked | 26,593 |
| Total search volume | 4,888,920/mo |
| Total estimated traffic | 43,129/mo |
| Keywords with CPC > 0 | 13,067 |
| Average CPC (when > 0) | €0.68 |
| Unique URLs ranked | ~2,500+ |

### 2.2 Search Intent Breakdown

| Intent | Keywords | % of Total |
|---|---|---|
| Informational | 24,609 | 92.5% |
| Transactional | 3,640 | 13.7% |
| Commercial | 1,788 | 6.7% |
| Navigational | 1,015 | 3.8% |

(Note: keywords can have multiple intents; percentages exceed 100%)

**Implication:** The overwhelming informational intent (92.5%) confirms this is a database/reference play, not an e-commerce play. We build authority through informational content, then monetize via affiliate links and ads.

### 2.3 Keyword Difficulty Distribution

| KD Range | Keywords | % |
|---|---|---|
| 0-10 (Very Easy) | 1,988 | 7.5% |
| 11-20 (Easy) | 17,128 | 64.4% |
| 21-30 (Moderate) | 6,423 | 24.2% |
| 31-40 (Medium) | 804 | 3.0% |
| 41-50 (Hard) | 166 | 0.6% |
| 51-60 (Very Hard) | 49 | 0.2% |
| 61+ (Extreme) | 35 | 0.1% |

**Key insight:** 96.1% of keywords have KD ≤ 30. This is an extremely low-competition niche. Programmatic SEO with proper entity-based content can dominate quickly.

### 2.4 Search Volume Distribution

| Volume Range | Keywords | % |
|---|---|---|
| 1-50 | 8,935 | 33.6% |
| 51-100 | 6,236 | 23.5% |
| 101-500 | 9,833 | 37.0% |
| 501-1,000 | 1,077 | 4.0% |
| 1,001-5,000 | 477 | 1.8% |
| 5,000+ | 35 | 0.1% |

### 2.5 Position Distribution (medidasdecoches.com)

| Position | Keywords | % |
|---|---|---|
| 1-3 | 5,954 | 22.4% |
| 4-10 | 3,569 | 13.4% |
| 11-20 | 3,242 | 12.2% |
| 21+ | 13,828 | 52.0% |

**Implication:** medidasdecoches.com ranks #1-3 for only 22% of its keywords. Over 52% are position 21+. There is massive room to outrank them with better content and page structure.

### 2.6 Top Keywords by Volume

| Keyword | Volume | KD | Intent |
|---|---|---|---|
| medidas de coches | 8,100 | 18 | informational |
| equivalencia neumaticos | 12,100 | 31 | informational |
| ford ranger raptor | 9,900 | 24 | informational |
| citroen c5 | 12,100 | 25 | informational |
| ford tourneo courier | 8,100 | 28 | navigational |
| fiat 500x | 8,100 | 29 | informational |
| medidas a5 | 6,600 | 29 | informational |
| citroen c4 picasso | 5,400 | 22 | informational |
| coches pequeños | 5,400 | 28 | informational |
| audi a5 sportback | 5,400 | 25 | informational |

### 2.7 Keyword Clusters

| Cluster | Keywords | Total Volume | Strategy |
|---|---|---|---|
| Medidas/dimensiones | 13,397 | 2,321,280 | Vehicle dimension pages (model pages) |
| Marca/modelo (brand names) | 4,066 | 964,130 | Brand + model landing pages |
| Maletero (trunk/boot) | 3,345 | 381,040 | Dedicated section on model pages |
| Motor/potencia | 375 | 61,460 | Engine specs on variant pages |
| Neumáticos/ruedas | 107 | 28,690 | Core tire fitment pages (our differentiator) |
| Peso/carga | 205 | 20,640 | Weight section on model pages |
| Comparativa | 184 | 20,330 | Comparison tool pages |
| Presión neumáticos | 71 | 16,130 | Tire pressure guide pages |
| Precio | 128 | 14,560 | Price reference + affiliate CTAs |
| Ficha técnica | 175 | 10,400 | Full spec sheet pages |
| Consumo/combustible | 73 | 5,690 | Fuel consumption on model pages |
| Other (long-tail) | 4,467 | 1,044,570 | Captured by comprehensive pages |

### 2.8 Quick Wins (KD < 30, Volume > 100)

**Total quick wins: 10,771 keywords | Combined volume: 3,596,120/mo**

Top quick wins for immediate targeting:

| Keyword | Volume | KD | Current competitor pos |
|---|---|---|---|
| medidas de coches | 8,100 | 18 | #1 (medidasdecoches.com) |
| ford ranger raptor | 9,900 | 24 | #32 |
| citroen c5 | 12,100 | 25 | #26 |
| fiat 500x | 8,100 | 29 | #51 |
| ford tourneo courier | 8,100 | 28 | #23 |
| medidas a5 | 6,600 | 29 | #34 |
| honda jazz | 6,600 | 24 | #45 |
| subaru outback | 6,600 | 28 | #90 |
| citroen c4 picasso | 5,400 | 22 | #14 |
| audi a5 sportback | 5,400 | 25 | #30 |
| medida neumatico | 590 | 19 | #1 |
| medida neumaticos | 320 | 20 | #1 |
| medidas ruedas | 260 | 21 | #2 |
| que neumaticos lleva mi coche | 390 | 16 | #35 |
| medidas ruedas coche | 210 | 23 | #1 |

### 2.9 Tire/Wheel-Specific Keywords (Our Core Differentiator)

180 tire/wheel keywords found in competitor data. Key ones:

| Keyword | Volume | KD | Opportunity |
|---|---|---|---|
| equivalencia neumaticos | 12,100 | 31 | Calculator tool page |
| neumaticos equivalentes | 2,400 | 34 | Same tool, alternate term |
| equivalencia de neumaticos | 1,300 | 38 | Same tool, alternate term |
| medida neumatico | 590 | 19 | Per-vehicle tire size page |
| equivalencias neumáticos | 590 | 26 | Calculator tool page |
| llantas y neumaticos | 480 | 18 | Category landing |
| que neumaticos lleva mi coche | 390 | 16 | Search/finder tool |
| comparador de neumaticos | 390 | 23 | Comparison tool |
| medida neumaticos | 320 | 20 | Per-vehicle tire size page |
| medidas ruedas | 260 | 21 | Wheel size pages |
| medidas ruedas coche | 210 | 23 | Wheel size by car |
| calcular equivalencia neumaticos | 210 | 17 | Calculator tool |

### 2.10 Top Brands by Keyword Count in Competitor Data

| Brand | Keywords | Priority |
|---|---|---|
| Toyota | 1,534 | ★★★ |
| Audi | 1,092 | ★★★ |
| BMW | 1,080 | ★★★ |
| Mercedes | 976 | ★★★ |
| Renault | 910 | ★★★ |
| Ford | 793 | ★★★ |
| Peugeot | 773 | ★★★ |
| Seat | 750 | ★★★ |
| Citroën | 743+166 | ★★★ |
| Opel | 737 | ★★★ |
| Kia | 716 | ★★★ |
| Volkswagen | 700 | ★★★ |
| Dacia | 658 | ★★★ |
| Hyundai | 644 | ★★★ |
| Mazda | 534 | ★★ |
| Fiat | 521 | ★★ |
| Volvo | 506 | ★★ |
| Škoda | 459 | ★★ |
| Nissan | 453 | ★★ |
| Cupra | 345 | ★★ |

---

## 3. Entity Model

### 3.1 Core Entity Hierarchy

```
Brand (marca)
  └─ Model (modelo)
       └─ Generation (generación / year range)
            └─ Variant (variante / motorización)
                 ├─ OEM Tire Sizes (medidas neumáticos originales)
                 ├─ Compatible Tire Sizes (medidas compatibles)
                 ├─ Wheel Specs (PCD, offset, hub bore)
                 └─ Technical Specs (motor, dimensiones, peso...)
```

### 3.2 Entity Definitions

**Brand (Marca)**
- slug, name, country, logo_url, wikipedia_url
- Models count, popular models list

**Model (Modelo)**
- slug, name, body_type (SUV, sedán, hatchback, familiar...)
- segment (utilitario, compacto, medio, grande, premium)
- production_years, current (boolean)
- Generations list

**Generation (Generación)**
- slug, name (e.g., "3ª generación (E90)")
- year_start, year_end
- facelift (boolean)
- photo_url
- Variants list

**Variant (Variante / Motorización)**
- slug, name (e.g., "2.0 TDI 150 CV")
- engine_code, displacement_cc, fuel_type
- power_hp, power_kw, torque_nm
- transmission (manual/auto), gears
- drive_type (FWD/RWD/AWD)
- length_mm, width_mm, height_mm, wheelbase_mm
- weight_kg, gross_weight_kg
- trunk_capacity_l, fuel_tank_l
- consumption_combined_l100km, co2_gkm
- top_speed_kmh, acceleration_0_100
- Tire fitment data (below)

**Tire Fitment (Medida Neumáticos)**
- tire_size_front (e.g., "205/55 R16")
- tire_size_rear (if different)
- rim_size_front (e.g., "6.5Jx16 ET45")
- rim_size_rear (if different)
- is_oem (boolean), is_optional (boolean)
- tire_pressure_front_bar, tire_pressure_rear_bar
- tire_pressure_front_loaded_bar, tire_pressure_rear_loaded_bar

**Wheel Specs (Especificaciones Llanta)**
- pcd (e.g., "5x112")
- center_bore_mm (e.g., 57.1)
- offset_min_mm, offset_max_mm
- wheel_torque_nm
- thread_size (e.g., "M14x1.5")
- bolt_type (bolt/nut)

### 3.3 Supplementary Entities

**Tire Size (Medida de Neumático)** — standalone entity for tire-centric pages
- width, aspect_ratio, construction, diameter
- load_index, speed_rating
- vehicles_using (reverse lookup)
- equivalent_sizes

**PCD / Bolt Pattern** — standalone for bolt pattern pages
- pcd_pattern (e.g., "5x112")
- vehicles_using (reverse lookup)

**Tire Pressure Guide** — per model/variant
- normal load, full load, highway recommendations

---

## 4. Information Architecture

### 4.1 Page Types & URL Structure

| Page Type | URL Pattern | Example | Est. Pages |
|---|---|---|---|
| Home | `/` | neumaticopedia.com | 1 |
| Brand Index | `/marcas` | /marcas | 1 |
| Brand Page | `/[brand]` | /toyota | ~50 |
| Model Page | `/[brand]/[model]` | /toyota/corolla | ~800 |
| Generation Page | `/[brand]/[model]/[gen]` | /toyota/corolla/2019-2023 | ~2,000 |
| Variant Page | `/[brand]/[model]/[gen]/[variant]` | /toyota/corolla/2019-2023/1-8-hybrid-122cv | ~6,000 |
| Tire Size Page | `/neumaticos/[size]` | /neumaticos/205-55-r16 | ~200 |
| Bolt Pattern Page | `/pcd/[pattern]` | /pcd/5x112 | ~30 |
| Tire Pressure Guide | `/presion-neumaticos/[brand]/[model]` | /presion-neumaticos/toyota/corolla | ~800 |
| Equivalence Calculator | `/equivalencia-neumaticos` | /equivalencia-neumaticos | 1 |
| Comparison Tool | `/comparar` | /comparar | 1 |
| Comparison Result | `/comparar/[car1]-vs-[car2]` | /comparar/seat-leon-vs-volkswagen-golf | dynamic |
| Body Type Hub | `/tipo/[type]` | /tipo/suv | ~10 |
| Blog/Guides | `/guia/[slug]` | /guia/como-leer-medidas-neumaticos | ~20 |
| Search Results | `/buscar` | /buscar?q=corolla | 1 |

**Estimated total pages at launch:** ~10,000  
**At full coverage (all brands/years):** ~50,000+

### 4.2 Navigation Structure

```
Header:
  Logo → /
  Marcas → /marcas (mega menu with top 20 brands)
  Neumáticos → /neumaticos (size index)
  Presión → /presion-neumaticos
  Equivalencias → /equivalencia-neumaticos
  Comparar → /comparar
  Guías → /guias
  🔍 Search

Footer:
  Brand columns (top 20)
  Tool links
  Legal/About
```

### 4.3 Breadcrumb Pattern

`Inicio > [Brand] > [Model] > [Generation] > [Variant]`  
Example: `Inicio > Toyota > Corolla > 2019-2023 (E210) > 1.8 Hybrid 122 CV`

---

## 5. Data Requirements

### 5.1 Primary Data Source: wheel-size.com API

**URL:** https://api.wheel-size.com/v2/  
**Tier:** Free (5,000 req/day)  
**Data available:**
- Makes (brands): GET /makes/
- Models by make: GET /models/
- Years by model: GET /years/
- Generations: GET /generations/
- Trims/variants: GET /trims/
- Tire/wheel data per trim: tire sizes, rim sizes, PCD, offset, center bore, bolt type, thread size, tire pressure

**Fields sourced:** tire_size_front, tire_size_rear, rim_size, pcd, center_bore, offset, wheel_torque, bolt_type, thread_size, tire_pressure

### 5.2 Technical Specs: Teoalida Car Database

**URL:** https://www.teoalida.com/cardatabase/  
**Format:** CSV purchase (~$50)  
**Data available:**
- Make, model, generation, variant
- Engine: displacement, fuel, power (HP/kW), torque, transmission
- Dimensions: length, width, height, wheelbase, ground clearance
- Weight: curb weight, GVWR
- Performance: top speed, 0-100 acceleration
- Consumption: combined L/100km
- Emissions: CO2 g/km
- Other: trunk capacity, fuel tank, doors, seats

**Fields sourced:** engine_code, displacement_cc, power_hp, torque_nm, fuel_type, transmission, dimensions, weight, consumption, emissions, trunk_capacity, fuel_tank

### 5.3 Vehicle Safety/Tech Data: NHTSA API

**URL:** https://vpic.nhtsa.dot.gov/api/  
**Tier:** Free, no auth required  
**Data available:**
- Decode VIN → all vehicle specs
- Get models by make
- Vehicle types, body classes
- Engine specs, fuel type, GVWR

**Fields sourced:** Supplementary cross-reference for US-market vehicles. Secondary source for engine specs, body type, GVWR.

### 5.4 Images & Basic Data: Wikipedia/Wikidata

**URL:** https://www.wikidata.org/wiki/Wikidata:Main_Page / https://commons.wikimedia.org/  
**Tier:** Free (CC-BY-SA)  
**Data available:**
- Vehicle images (Wikimedia Commons)
- Model descriptions
- Production years
- Brand logos
- Wikidata IDs for structured data

**Fields sourced:** photo_url, brand_logo, description_text, production_year_start/end

### 5.5 Spanish Homologation: DGT/ITV Data

**URL:** https://sede.dgt.gob.es/ (scraping required)  
**Data available:**
- Spanish market homologated tire sizes
- Vehicle type approval data
- ITV inspection requirements

**Fields sourced:** Spanish-specific homologated alternative sizes, ITV-relevant specs

### 5.6 Phase 2 — Nearby Tire Shops: OpenStreetMap/Nominatim

**URL:** https://nominatim.openstreetmap.org/  
**Tier:** Free (usage policy: 1 req/sec)  
**Data available:**
- Tire shops by location
- Shop names, addresses, phone numbers

**Fields sourced:** Nearby tire shop recommendations (geolocation-based feature)

### 5.7 Data Pipeline Summary

| Data Field | Primary Source | Secondary Source |
|---|---|---|
| Tire sizes (OEM + compatible) | wheel-size.com API | DGT/ITV |
| PCD, offset, hub bore | wheel-size.com API | — |
| Tire pressure | wheel-size.com API | Owner manuals |
| Engine specs | Teoalida CSV | NHTSA API |
| Dimensions | Teoalida CSV | wheel-size.com |
| Weight | Teoalida CSV | NHTSA API |
| Consumption/emissions | Teoalida CSV | — |
| Photos | Wikimedia Commons | — |
| Brand/model metadata | wheel-size.com API | Wikipedia |
| Prices (approx.) | Manual research | — |

---

## 6. Page-Level Specifications

### 6.1 Home Page (`/`)

**Purpose:** Primary landing, brand-level navigation, search  
**Target keyword:** "medidas neumaticos coche" / "neumaticos por coche"

**Layout:**
1. Hero section with search bar ("¿Qué neumáticos lleva tu coche?")
2. Brand selector: Make → Model → Year → Variant dropdowns (cascading)
3. Popular brands grid (top 20 logos, clickable)
4. Recent/popular searches sidebar
5. Quick access tools: Equivalence calculator, Pressure guide, Comparison
6. Latest articles/guides
7. SEO text block (200-300 words about the site)

**SEO Template:**
- Title: `Neumáticos por coche: medidas, presión y equivalencias | Neumaticopedia`
- H1: `Encuentra los neumáticos de tu coche`
- Meta description: `Base de datos de neumáticos por marca, modelo y año. Consulta medidas originales, equivalencias, presión recomendada y especificaciones de llantas para tu vehículo.`

**Internal links:** All brand pages, tool pages, top model pages

### 6.2 Brand Index Page (`/marcas`)

**Purpose:** Full brand directory  
**Target keyword:** "marcas de coches"

**Layout:**
1. Alphabetical brand grid with logos
2. Filter by country/region
3. Brand count badge (models per brand)
4. Search within brands

**SEO Template:**
- Title: `Todas las marcas de coches: neumáticos y medidas | Neumaticopedia`
- H1: `Marcas de coches`

### 6.3 Brand Page (`/[brand]`)

**Purpose:** Brand hub with all models  
**Target keywords:** "[brand] medidas", "[brand] neumaticos"

**Layout:**
1. Brand header: logo, country, description
2. Model grid with thumbnails, organized by segment
3. Filter/sort: by type (SUV, sedan...), by alphabetical, by popularity
4. Current models highlighted, discontinued in separate section
5. Brand stats: models count, popular tire sizes for this brand
6. Most common PCD patterns for this brand

**Content blocks:**
- Brand overview (auto-generated + editorial, 150 words)
- Quick facts table (headquarters, founded, models in Spain)
- Common tire sizes for [brand] vehicles

**SEO Template:**
- Title: `[Brand]: medidas de neumáticos y llantas por modelo | Neumaticopedia`
- H1: `Neumáticos y medidas de [Brand]`
- Meta: `Consulta las medidas de neumáticos, presión y llantas para todos los modelos de [Brand]. Datos de [N] modelos actualizados a 2025.`

**Internal links:** All model pages for this brand, related brands (same segment), brand index

### 6.4 Model Page (`/[brand]/[model]`)

**Purpose:** Central model hub — THE money page  
**Target keywords:** "[brand] [model] medidas", "medidas [model]", "[brand] [model] neumaticos", "[model] maletero", "[model] dimensiones"

**Layout:**
1. Model header: photo, brand crumb, model name, years
2. Generation selector tabs (e.g., "2019-2023 | 2014-2018 | 2009-2013")
3. **Tire sizes summary table** (all generations, most common sizes)
4. **Dimensions card**: length × width × height visual diagram
5. **Trunk capacity**: liters, comparison bar vs segment average
6. Variant table: all motorizations with key specs
7. **Tire pressure quick reference** table
8. **Wheel specs summary**: PCD, center bore, offset range
9. SEO text block (300-500 words, auto-generated per model)
10. Related models (same segment) sidebar
11. **Affiliate CTA**: "Comprar neumáticos para [Brand] [Model]" → affiliate links

**Data fields displayed:**
- Dimensions: length, width, height, wheelbase (mm)
- Weight: curb weight, GVWR (kg)
- Trunk: capacity (L), with seats down
- Engine options: list with power, fuel type
- Tire sizes: table of all OEM sizes by variant
- Tire pressure: front/rear, normal/loaded (bar)
- Wheel: PCD, center bore, offset range
- Fuel: consumption, tank capacity, CO2

**SEO Template:**
- Title: `[Brand] [Model]: medidas neumáticos, dimensiones y ficha técnica | Neumaticopedia`
- H1: `[Brand] [Model]: neumáticos, medidas y especificaciones`
- Meta: `Medidas de neumáticos del [Brand] [Model]: [tire_size]. Dimensiones: [L]x[W]x[H] mm. Maletero: [trunk]L. Presión: [pressure] bar. Toda la ficha técnica.`

**Internal links:** Generation pages, variant pages, tire size pages, PCD page, brand page, pressure guide, comparison ("comparar con [rival]")

**Interactive elements:**
- Generation tab switcher
- Dimension comparison slider (vs segment average)
- "¿Cuál es tu variante?" dropdown → scrolls to relevant row

### 6.5 Generation Page (`/[brand]/[model]/[gen]`)

**Purpose:** Detailed specs for a specific generation  
**Target keywords:** "[brand] [model] [year] medidas", "[model] [gen name]"

**Layout:**
1. Generation header with photo
2. All variants table with full specs
3. **Tire fitment matrix**: variant × tire size (OEM/optional)
4. Detailed dimensions diagram
5. **Compatible tire sizes** (non-OEM alternatives that fit)
6. Wheel torque specs
7. Common maintenance data

**SEO Template:**
- Title: `[Brand] [Model] [year_start]-[year_end]: neumáticos, medidas y ficha técnica`
- H1: `[Brand] [Model] [gen_name] ([year_start]-[year_end])`

### 6.6 Variant Page (`/[brand]/[model]/[gen]/[variant]`)

**Purpose:** Most granular vehicle page — full spec sheet  
**Target keywords:** "[brand] [model] [engine] ficha tecnica", "[model] [engine] neumaticos"

**Layout:**
1. Variant header with full name
2. **Complete tire fitment data**: OEM sizes, optional sizes, compatible sizes
3. **Full spec table**: engine, performance, dimensions, weight, consumption
4. **Tire pressure card**: visual tire diagram with pressures per axle
5. **Wheel specs card**: PCD diagram, bolt pattern visual
6. **Affiliate block**: "Comprar neumáticos [tire_size] para [Brand] [Model]"
7. Similar variants comparison

**Data fields (complete):**
- Engine: code, displacement, fuel, power HP/kW, torque, transmission, gears, drive
- Performance: top speed, 0-100
- Dimensions: L×W×H, wheelbase, ground clearance
- Weight: curb, GVWR
- Capacity: trunk (L), fuel tank (L), seats
- Consumption: urban/highway/combined (L/100km), CO2
- Tires: front size, rear size (if different), OEM/optional flag
- Wheels: rim size, PCD, center bore, offset, torque, bolt type, thread
- Pressure: front/rear, normal/loaded

**SEO Template:**
- Title: `[Brand] [Model] [engine]: neumáticos [tire_size], ficha técnica completa`
- H1: `[Brand] [Model] [variant_name]`

### 6.7 Tire Size Page (`/neumaticos/[size]`)

**Purpose:** Reverse lookup — "what cars use this tire size?"  
**Target keywords:** "neumaticos [size]", "[size] que coches", "205 55 r16"

**Layout:**
1. Tire size header with visual diagram (width, profile, diameter)
2. **Explanation**: what each number means
3. **Vehicles that use this size** — grouped by brand
4. **Equivalent sizes** with comparison table
5. **Buy this size** — affiliate links to tire shops
6. Compatible rim sizes

**SEO Template:**
- Title: `Neumáticos [size]: qué coches los usan y equivalencias | Neumaticopedia`
- H1: `Neumáticos [size]`

**Internal links:** All vehicle pages using this size, equivalent size pages

### 6.8 Bolt Pattern Page (`/pcd/[pattern]`)

**Purpose:** All vehicles sharing a bolt pattern  
**Target keywords:** "pcd [pattern]", "5x112 que coches"

**Layout:**
1. PCD visual diagram
2. Explanation of what PCD means
3. Vehicles grouped by brand using this pattern
4. Compatible wheel brands/models
5. Related PCDs (close but incompatible)

**SEO Template:**
- Title: `PCD [pattern]: todos los coches con anclaje [pattern] | Neumaticopedia`
- H1: `Anclaje [pattern] (PCD)`

### 6.9 Tire Pressure Guide (`/presion-neumaticos/[brand]/[model]`)

**Purpose:** Dedicated pressure reference per model  
**Target keywords:** "presion neumaticos [brand] [model]", "presion [model]"

**Layout:**
1. Model header
2. **Pressure table** by variant, tire size, and load condition
3. Visual tire diagram with pressures
4. Where to find pressure info in your car (door sticker, manual)
5. General pressure tips
6. TPMS warning explanation

**SEO Template:**
- Title: `Presión neumáticos [Brand] [Model]: tabla por variante y carga`
- H1: `Presión de neumáticos del [Brand] [Model]`

### 6.10 Equivalence Calculator (`/equivalencia-neumaticos`)

**Purpose:** Interactive calculator tool  
**Target keywords:** "equivalencia neumaticos" (12,100 vol!), "calcular equivalencia neumaticos"

**Layout:**
1. Two tire size input fields (original → alternative)
2. **Real-time comparison**: diameter difference %, speedometer error, ground clearance change
3. Visual overlay of both tire profiles
4. ITV compatibility warning (Spain-specific: max 3% diameter deviation)
5. Pre-calculated popular equivalences table
6. "¿Qué equivalencias tiene tu neumático?" search

**SEO Template:**
- Title: `Calculadora de equivalencia de neumáticos | Neumaticopedia`
- H1: `Equivalencia de neumáticos: calculadora online`

**Interactive elements:**
- Real-time calculation as user types
- Visual tire profile comparison (SVG/Canvas)
- Share result URL

### 6.11 Comparison Tool (`/comparar`)

**Purpose:** Side-by-side vehicle comparison  
**Target keywords:** "comparar coches medidas", "[car1] vs [car2]"

**Layout:**
1. Two vehicle selector dropdowns
2. Side-by-side spec table
3. Visual dimension overlay
4. Tire/wheel differences highlighted
5. "Winner" badges per category

**SEO Template:**
- Title: `Comparar [Car1] vs [Car2]: medidas, neumáticos y ficha técnica`
- H1: `[Car1] vs [Car2]: comparativa`

### 6.12 Body Type Hub (`/tipo/[type]`)

**Purpose:** Browse vehicles by category  
**Target keywords:** "suv medidas", "coches pequeños dimensiones"

**Layout:**
1. Type description and characteristics
2. Vehicle grid filterable by brand, year, price range
3. Size comparison chart (all models overlaid)
4. Most popular tire sizes in this category

**SEO Template:**
- Title: `[Type] en España: medidas, dimensiones y neumáticos de todos los modelos`
- H1: `Todos los [type]: medidas y neumáticos`

### 6.13 Blog/Guides (`/guia/[slug]`)

**Purpose:** Editorial content for informational long-tail  
**Target keywords:** "como leer medidas neumaticos", "que significan los numeros del neumatico"

**Layout:**
1. Article with structured H2/H3 headings
2. Visual diagrams and infographics
3. Related tools CTAs
4. Related vehicle pages
5. FAQ schema

**Initial guides planned:**
- Cómo leer las medidas de un neumático
- Qué es el PCD y cómo medirlo
- Tabla de presión de neumáticos por marca
- Equivalencias de neumáticos: guía completa
- Cuándo cambiar los neumáticos: señales y normativa
- Neumáticos de invierno vs verano en España

---

## 7. Design & UX Direction

### 7.1 Design Principles

1. **Data-first:** Tables, specs, and numbers are the hero — not marketing fluff
2. **Scannable:** Users come for one data point. Make it findable in 3 seconds
3. **Trust signals:** Clean, professional layout says "reliable database"
4. **Mobile-first:** 65%+ traffic will be mobile (checking tire size at the shop)
5. **Fast:** Static generation, no client-side data fetching for core content

### 7.2 Visual Style

- **Color palette:** Dark navy (#1a2332) + electric blue accent (#2563eb) + white cards
- **Typography:** Inter or similar clean sans-serif, monospace for specs/numbers
- **Icons:** Outline style, automotive-themed (tire, wheel, car silhouettes)
- **Cards:** Rounded corners, subtle shadows, data-dense but organized
- **Tables:** Zebra-striped, sticky headers, responsive (horizontal scroll on mobile)

### 7.3 Key UX Components

- **Vehicle Finder Widget:** Cascading dropdowns (Make → Model → Year → Variant). Appears on home, in header (collapsed), and on relevant pages. Autocomplete search alternative.
- **Tire Size Visual:** SVG diagram showing tire width, profile, diameter with labeled measurements
- **PCD Diagram:** Visual bolt pattern with measurements
- **Dimension Overlay:** Side/top view car silhouette with dimension lines
- **Pressure Card:** Four-tire layout with pressure values per corner
- **GatedLink Component:** For unpublished pages — shows the link text but as non-clickable span with "Próximamente" tooltip, so crawlers see the entity relationship but users don't hit 404s

### 7.4 Responsive Strategy

- **Mobile (< 768px):** Single column, collapsible spec sections, sticky CTA bar at bottom
- **Tablet (768-1024px):** Two-column layout, side-by-side comparison possible
- **Desktop (> 1024px):** Three-column with sidebar (related models, affiliate CTAs)

---

## 8. SEO Strategy

### 8.1 Technical SEO

- **Rendering:** Static Site Generation (SSG) via Next.js App Router — pre-rendered HTML
- **Core Web Vitals:** Target LCP < 1.5s, CLS < 0.05, INP < 100ms
- **Sitemap:** Dynamic XML sitemap split by brand (/sitemap-toyota.xml, etc.)
- **Robots.txt:** Allow all, exclude /buscar, /api
- **Canonical URLs:** Self-referencing on all pages
- **hreflang:** es-ES initially, prep for es-MX, es-AR later
- **Internal linking:** Every entity links to parent, children, siblings, and related entities

### 8.2 Structured Data (Schema.org)

| Page Type | Schema | Properties |
|---|---|---|
| Brand Page | Organization + ItemList | name, logo, url, itemListElement (models) |
| Model Page | Car + Product | brand, model, vehicleConfiguration, fuelType |
| Variant Page | Car (detailed) | All specs as properties |
| Tire Size Page | Product | name, size, description |
| Guides | Article + FAQ | headline, author, datePublished, mainEntity |
| Comparison | ItemList | Two Car entities |
| Calculator | WebApplication | name, applicationCategory |

### 8.3 Content Strategy

**Programmatic content (90% of pages):**
- Auto-generated from structured data
- Template-based but with variation (multiple sentence templates per data point)
- Spanish natural language: "El Toyota Corolla 2019-2023 monta neumáticos 205/55 R16 de serie, con una presión recomendada de 2.3 bar en el eje delantero."
- Unique per variant (different data = different content)

**Editorial content (10%):**
- Guides and how-tos (targeting informational long-tail)
- Seasonal content (winter tires guide, summer check, etc.)
- Brand comparison articles

### 8.4 Link Building Strategy

1. **Digital PR:** "Infographic: the most popular tire sizes in Spain 2025" → automotive blogs
2. **Tool links:** Equivalence calculator is naturally linkable (useful tool)
3. **Forum participation:** Answering tire questions on ForoCoches, ClubGolf, etc. with neumaticopedia links
4. **Data citations:** Offer data embeds/widgets to automotive bloggers
5. **HARO/Connectively:** Expert source for tire/automotive queries

### 8.5 Keyword Targeting Priority

**Phase 1 — Quick wins (Month 1-3):**
- Brand + model pages for top 20 brands (KD 18-28)
- Core tool pages (equivalence calculator, pressure guide)
- "medidas [model]" pattern (10,000+ keywords)

**Phase 2 — Expansion (Month 3-6):**
- All generation and variant pages
- Tire size reverse-lookup pages
- PCD/bolt pattern pages
- Body type hubs

**Phase 3 — Authority (Month 6-12):**
- Editorial guides and long-form content
- Comparison pages (pre-generated popular matchups)
- International expansion prep (LATAM)

---

## 9. Publication Strategy

### 9.1 Launch Plan

**Pre-launch (Week 1-2):**
- Deploy Next.js app shell with home, brand index, search, tools
- Ingest data from wheel-size.com API + Teoalida CSV
- Generate static JSON files for all entities

**Phase 1 — Top 20 Brands (Week 3-6):**
Publishing 20-30 pages/day, prioritized by:
1. Search volume (from Semrush data)
2. Keyword difficulty (lowest first)
3. Brand popularity in Spain

**Priority brand order:**
1. Toyota (1,534 kws)
2. Volkswagen (700 kws + most sold in Spain)
3. Seat/Cupra (750+345 kws, Spanish brand loyalty)
4. Hyundai (644 kws)
5. Kia (716 kws)
6. Peugeot (773 kws)
7. Renault (910 kws)
8. Citroën (909 kws)
9. BMW (1,080 kws)
10. Audi (1,092 kws)
11. Mercedes (976 kws)
12. Ford (793 kws)
13. Dacia (658 kws)
14. Opel (737 kws)
15. Nissan (453 kws)
16. Mazda (534 kws)
17. Fiat (521 kws)
18. Škoda (459 kws)
19. Volvo (506 kws)
20. Honda (292 kws)

**Per brand, publish in order:**
1. Brand page
2. Top 5 models by search volume (model pages)
3. Current generations for those models
4. All variants for current generations
5. Remaining models
6. Historical generations

**Phase 2 — Extended Brands (Week 7-12):**
- Remaining brands (Mini, Lexus, Jeep, Suzuki, Tesla, Subaru, Mitsubishi, etc.)
- All tire size pages
- All PCD pages
- Comparison tool with pre-generated comparisons

**Phase 3 — Content & Authority (Month 3-6):**
- Editorial guides (1-2 per week)
- Seasonal content
- User-requested models/variants

### 9.2 Progressive Publication System

- Each entity has a `publishedAt` date field
- `GatedLink` component renders:
  - Published → normal `<a>` tag with href
  - Unpublished → `<span>` with title text (no link, no 404)
- Sitemap only includes published pages
- Unpublished pages return 404 (not soft 404, not noindex)
- Publication queue managed via JSON manifest file

### 9.3 Content Velocity Targets

| Timeframe | Pages Published | Cumulative |
|---|---|---|
| Month 1 | 600 | 600 |
| Month 2 | 600 | 1,200 |
| Month 3 | 600 | 1,800 |
| Month 6 | — | 4,000 |
| Month 12 | — | 10,000 |

---

## 10. Competitive Advantages

### 10.1 vs. medidasdecoches.com (#1 competitor)

| Factor | medidasdecoches.com | neumaticopedia.com |
|---|---|---|
| Focus | Car dimensions (general) | Tire/wheel fitment (specialized) |
| Tire data | Minimal | Complete (OEM + compatible + pressure) |
| Wheel specs | None | PCD, offset, hub bore, torque |
| Equivalences | None | Interactive calculator |
| UX/Design | Dated PHP site | Modern Next.js, mobile-first |
| Speed | Slow server-rendered | Static, < 1.5s LCP |
| Structured data | Basic | Full Schema.org Car + Product |
| Comparison tool | Basic dimensions only | Full specs + tire/wheel |

### 10.2 vs. wheel-size.com / llantasneumaticos.com

| Factor | wheel-size.com | neumaticopedia.com |
|---|---|---|
| Language | English (llantasneumaticos = poor Spanish) | Native Spanish, Spain-focused |
| UX | Complex, cluttered | Clean, data-first, scannable |
| Cross-referenced data | Tire/wheel only | + engine, dimensions, consumption, weight |
| Tire pressure | Basic | Detailed (loaded/unloaded, per variant) |
| Equivalence tool | None | Interactive calculator |
| Spanish homologation | No | ITV/DGT data |
| Content quality | Machine-translated | Native Spanish editorial |
| Local SEO | No | Spain-specific (DGT data, local shops) |

### 10.3 vs. presion-de-neumaticos.es

| Factor | presion-de-neumaticos.es | neumaticopedia.com |
|---|---|---|
| Scope | Pressure only | Full fitment + specs + pressure |
| Depth | Basic pressure tables | Per-variant, loaded/unloaded |
| Additional data | None | Complete technical specs |
| Tools | None | Calculator, comparison, finder |

### 10.4 Unique Value Proposition

**"The only Spanish-language site that combines tire fitment data, wheel specifications, vehicle dimensions, and technical specs in one place — with interactive tools and modern UX."**

Key differentiators:
1. **Cross-referenced data nobody else combines:** Tire sizes + PCD + pressure + engine specs + dimensions + consumption — all on one page per variant
2. **Native Spanish with Spain-specific data:** ITV homologation, DGT references, Spanish tire shop affiliates
3. **Interactive tools:** Equivalence calculator (targeting 12,100 vol keyword), comparison tool, vehicle finder
4. **Modern tech stack:** Sub-2-second loads, mobile-first, proper structured data
5. **Programmatic scale:** 10,000+ unique pages from structured data, each genuinely useful
6. **Monetization-ready from day 1:** Affiliate CTAs naturally integrated into data pages (buy the tires you just looked up)

### 10.5 Risk Assessment

| Risk | Probability | Mitigation |
|---|---|---|
| wheel-size.com API rate limits | Medium | Pre-fetch all data, cache as static JSON, daily delta updates |
| Google algorithm penalizes thin programmatic content | Low | Ensure unique data combinations per page, add editorial layer |
| Competitor copies our approach | Medium | First-mover advantage in Spanish market, build authority fast |
| Data accuracy issues | Medium | Multiple source cross-referencing, user feedback mechanism |
| LATAM Spanish vs Spain Spanish conflicts | Low | Use es-ES initially, separate templates for LATAM later |

---

*Brief prepared by Strategist based on analysis of 26,593 organic keywords from medidasdecoches.com (Semrush ES), plus seed keyword research on "neumáticos" and "llantas" clusters (30K+ keywords total). Ready for CEO review.*
