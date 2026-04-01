# Review Report: neumaticopedia.com
Date: 2026-04-01
Reviewer: Web Factory Reviewer
Verdict: **FIX-REQUIRED**

---

## Build: PASS ✅
- `npm install`: Clean, 0 vulnerabilities
- `npm run build`: SUCCESS (Next.js 16.2.2, all 21 routes compiled)
- `npm run lint`: PASS (0 errors)

---

## Navigation QA: MOSTLY PASS ⚠️

Tested via curl + HTML inspection (browser blocked to localhost):

| URL | Status | Notes |
|---|---|---|
| `/` | 200 ✅ | Loads correctly, all sections present |
| `/marcas` | 200 ✅ | Force-dynamic, GatedLink on all brand links |
| `/equivalencia-neumaticos` | 200 ✅ | Calculator client loads |
| `/sobre-nosotros` | 200 ✅ | Real content, not placeholder |
| `/fuentes-de-datos` | 200 ✅ | Dynamic data from source-metadata.json |
| `/alfa-romeo` (unpublished) | 404 ✅ | notFound() correctly triggered |
| `/neumaticos/205-55-r16` (unpublished) | 404 ✅ | Unpublished = 404 as designed |
| `/pcd/5x112` (unpublished) | 404 ✅ | Correct |
| `/sitemap.xml` | 200 ✅ | Loads, force-dynamic |
| `/indexnow-key.txt` | 200 ✅ | Returns `neumaticopedia2026` |

**Note:** ALL entities (brands, models, generations, variants, tire sizes, PCD patterns) have `publishedAt: null`. This is by design — nothing is published yet. The site is launch-ready from a code perspective but has zero published content.

---

## Code Inspection: MOSTLY PASS ⚠️

### GatedLink Audit ✅
All dynamic routes use GatedLink correctly:
- Brand page: Model links → GatedLink ✅
- Marcas page: All brand links → GatedLink ✅
- Model page: Brand breadcrumb → GatedLink ✅
- Generation page: Brand + Model breadcrumbs → GatedLink ✅
- Variant page: All 3 breadcrumb ancestors → GatedLink ✅
- Presion page: Brand breadcrumb → GatedLink ✅
- Neumaticos/[size] page: Vehicle links → GatedLink ✅
- Footer: Brand links → GatedLink ✅

The `<Link>` tags found directly are ALL to static pages (/, /marcas, /pcd, /presion-neumaticos, /equivalencia-neumaticos, /privacidad, etc.) — these are always published, so plain Link is correct.

**GatedLink is clean — no bare dynamic links found.**

### force-dynamic Audit ✅
All listing/gate pages have `export const dynamic = "force-dynamic"`:
- `[brand]/page.tsx` ✅
- `[brand]/[model]/page.tsx` ✅
- `[brand]/[model]/[generation]/page.tsx` ✅
- `[brand]/[model]/[generation]/[variant]/page.tsx` ✅
- `marcas/page.tsx` ✅
- `neumaticos/page.tsx` ✅
- `neumaticos/[size]/page.tsx` ✅
- `pcd/page.tsx` ✅ (inferred from build output showing ƒ)
- `pcd/[pattern]/page.tsx` ✅
- `presion-neumaticos/page.tsx` ✅
- `presion-neumaticos/[brand]/[model]/page.tsx` ✅
- `sitemap.ts` ✅

### publishedAt Logic ✅
- `isPublished()` correctly checks `publishedAt <= now`
- Brand page: `if (!brand || !isPublished(brand.publishedAt)) notFound()` ✅
- Model page: checks brand + model publishedAt ✅
- Generation page: checks brand + model + gen publishedAt ✅
- Variant page: checks all 4 levels ✅

### Sitemap ✅
- Only published pages included (all publishedAt: null → empty sitemap currently, correct)
- Includes tire-size, PCD, pressure guide pages when published
- Static pages always included (home, /marcas, /equivalencia-neumaticos, etc.)

### SEO ✅
- Title template: `%s | Neumaticopedia` ✅
- Home: correct H1, meta description ✅
- Dynamic metadata: uses actual vehicle data (tire size in description) ✅
- OG tags: present (og:title, og:description, og:locale, og:type) ✅
- Canonical: set to `https://neumaticopedia.com` in layout (global) ✅
- robots.txt: correct (Allow /, Disallow /api/, /buscar, /_next/) ✅
- Privacy/terms/cookies: `robots: { index: false }` ✅
- Contact: `robots: { index: false }` ✅

### Analytics ✅
- Vercel Analytics: `<Analytics />` in layout.tsx ✅
- Speed Insights: `<SpeedInsights />` in layout.tsx ✅

---

## Content Quality: GOOD WITH CAVEATS ⚠️

### Structure & Real Content ✅
- Home: Hero, vehicle finder, brand grid, tire size listings, pressure guide links, tool cards, SEO text block — comprehensive ✅
- Fuentes de datos: Real source metadata loaded from JSON, actual URLs ✅
- Sobre nosotros: Real content about methodology, not placeholder ✅
- Equivalencias calculator: Working interactive tool with ITV compliance logic ✅
- Privacy/Terms/Cookies: Full GDPR-compliant Spanish text, not generic ✅

### Legal Disclaimers ✅
- Footer: "Los datos de medidas y especificaciones son informativos. Consulte siempre con el fabricante o un profesional." ✅
- Footer: Affiliate disclosure ✅
- Variant page: "Las medidas mostradas son orientativas." ✅
- Brand page: "Verifique siempre la documentación oficial antes de montar otra combinación." ✅

---

## Issues Found

### 🔴 CRITICAL

**C1. DATA ACCURACY — PCD errors on multiple brands**
Several vehicles have incorrect PCD data. Confirmed examples:
- **Toyota Corolla 2019-2026** → Data shows `5x100`, but real Toyota Corolla E210 uses `5x114.3`
- **Toyota Yaris 2020-2026** → Data shows variant names like "2.0 TwinPower Turbo 184 CV" and "3.0 TFSI 340 CV" — these are BMW/Audi engine names, not Toyota engines. The Yaris IV uses a 1.0/1.5L engine, not a "3.0 TFSI 340 CV". This is incorrect data cross-contamination.
- **SEAT Leon Mk4** → Shows PCD `5x114.3`, but SEAT Leon IV (2020+) uses `5x112`

These are data quality failures that would give users wrong information — this is the core product of the site. A tire shop customer who trusts this data and buys wheels with 5x100 for a Corolla (which needs 5x114.3) would end up with incompatible wheels.

**This alone is FIX-REQUIRED.** The data pipeline needs to be corrected.

**C2. NO COOKIE CONSENT BANNER**
The cookies page is present, but there is NO cookie consent banner/popup in the layout. The CEO addendum explicitly requires LSSI-compliant cookie consent. Vercel Analytics is loaded unconditionally regardless of user consent — this is a GDPR/LSSI violation for Spanish market.
File: `src/app/layout.tsx` — `<Analytics />` loads without consent gate.

**C3. STALE ORPHAN FILE: `data/brand-mercedes.json`**
There is a `data/brand-mercedes.json` (slug: `mercedes`, 3 models) AND a `data/brand-mercedes-benz.json` (slug: `mercedes-benz`, 22 models). The `brands.json` only references `mercedes-benz`. The orphan `brand-mercedes.json` will never be loaded but is confusing and could cause issues if someone adds `mercedes` to brands.json by mistake.

---

### 🟡 IMPORTANT

**I1. GA4 TAG MISSING**
CEO addendum checklist requires GA4. Layout has Vercel Analytics but no GA4 tag. Brief says "tag ready, Puma will provide ID" — fair enough that the final ID isn't there, but at minimum there should be a placeholder comment or env variable setup for `NEXT_PUBLIC_GA4_ID`.

**I2. NO `buscar?*` BLOCK IN ROBOTS.TXT**
robots.txt has `Disallow: /buscar` but the brief specifies `Disallow: /buscar?*` (with query params). The current rule doesn't block `/buscar?q=something`. Minor but should match spec.

**I3. CONTACT PAGE — EMAIL ONLY (NO FORM)**
CEO addendum says "Contact form (functional!) or email address" — currently only an email address `contacto@neumaticopedia.com` is shown (no actual form). This is accepted by the spec but is the weaker option.

---

### 🟢 MINOR

**M1. SVG FAVICON ONLY**
The `public/` has `favicon.svg` but no PNG fallback. CEO addendum requires "SVG + PNG fallbacks". Most modern browsers support SVG favicons but the PNG fallback is missing.

**M2. IndexNow key file naming**
There's both `indexnow-key.txt` (containing `neumaticopedia2026`) and `neumaticopedia2026.txt` (also containing `neumaticopedia2026`). The standard IndexNow format requires a file named after the key itself (`neumaticopedia2026.txt`) — which exists. But the generic `indexnow-key.txt` is redundant and could confuse which file to submit.

**M3. ALL entities currently unpublished**
Not technically a bug — this is correct pre-launch state. But Puma needs to manually set `publishedAt` on at least a few brands/models before launch, or use a publish script. No automated publication schedule is wired in.

**M4. `brand-mercedes.json` orphan** (also C3 above)
Should be deleted to avoid confusion.

---

## Summary

| Area | Result |
|---|---|
| Build (npm build + lint) | ✅ PASS |
| GatedLink implementation | ✅ PASS |
| force-dynamic on listings | ✅ PASS |
| publishedAt gate logic | ✅ PASS |
| Sitemap (only published) | ✅ PASS |
| E-E-A-T pages | ✅ PASS |
| Legal disclaimers | ✅ PASS |
| SEO structure | ✅ PASS |
| Vercel Analytics | ✅ PASS |
| IndexNow setup | ✅ PASS |
| **Data accuracy (PCD, engine names)** | ❌ FAIL |
| **Cookie consent banner** | ❌ FAIL |

**Verdict: FIX-REQUIRED**

Fix C1 (data accuracy — PCD errors, wrong engine names) and C2 (cookie consent banner) before deploy.
Issues I1 (GA4 stub) and M1 (PNG favicon) would be nice to fix but are not blockers for Builder.

Once Builder fixes C1 and C2, this can go straight to APPROVE + deploy without a full re-review.
