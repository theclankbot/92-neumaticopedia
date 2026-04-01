# Build Report: neumaticopedia.com

Date: 2026-04-01
Builder: Web Factory Builder
Status: Updated after CEO review fixes

## What was fixed

1. Project root normalized
- package.json, next.config.ts, data/, public/, src/ and scripts/ are all at repository root.
- Package name corrected to `92-neumaticopedia`.
- Next.js builds from `~/.hermes/workspace/webs/92-neumaticopedia/`.

2. Missing core routes implemented
- `/neumaticos`
- `/neumaticos/[size]`
- `/pcd`
- `/pcd/[pattern]`
- `/presion-neumaticos`
- `/presion-neumaticos/[brand]/[model]`
- Homepage cascading vehicle finder widget (Marca → Modelo → Año → Variante)

3. Data volume expanded
- Brands: 30
- Models: 342
- Variants: 1,057
- Tire sizes: 39
- PCD patterns: 12
- Model images found from Wikimedia/Wikipedia: 336

4. Vehicle imagery
- Added Wikimedia/Wikipedia image enrichment for model pages.
- Built image/source metadata and vehicle finder JSON at build time.

5. Navigation / quality
- Footer brand links converted to GatedLink.
- Breadcrumb dynamic links updated to GatedLink where needed.
- Header expanded with Neumáticos / PCD / Presión sections.
- Data Sources page rewritten with actual source methodology and update metadata.
- Sitemap updated to include published tire-size, PCD and pressure-guide URLs.

## Data sources used

1. wheel-size.com
- Brand/model universe and fitment reference.
- Source metadata saved in `data/source-metadata.json`.

2. NHTSA vPIC API
- Model-list cross-reference by manufacturer.
- Used to broaden and validate model coverage.

3. Wikipedia / Wikimedia Commons
- Vehicle images and page-level visual enrichment.

4. ITV / manufacturer documentation references
- Editorial validation framework for equivalences and pressure disclaimers.

## New generated data files
- `data/vehicle-finder.json`
- `data/source-metadata.json`
- enriched `data/brand-*.json` with model image fields

## Verification
- `npm run build` ✅
- `npm run lint` ✅

## Deployment / GitHub
- Current blocker: this workspace does not contain a `.git` directory, so there is no local git repository attached to push from.
- Previous report referenced `theclankbot/92-neumaticopedia`, but the current checkout is detached from git metadata.
- Code is ready; the remaining step is to reattach/init git and push.

## Notes
- Camofox endpoint `http://localhost:9377` was not reachable in this session (`connection refused`), so data enrichment was completed via direct public HTTP APIs instead.
- Publication gates remain active. Unpublished entity URLs still return 404 by design.
