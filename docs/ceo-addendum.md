# CEO Addendum — Builder Requirements

This document supplements project-brief.md with mandatory requirements the Builder MUST implement from day one. No exceptions, no "phase 2".

---

## 1. Progressive Publication (CRITICAL)

### publishedAt System
- Every entity (brand, model, generation, variant) has a `publishedAt` field
- `null` = not published = Coming Soon UI
- ISO date string = published = full content
- This is the ONLY mechanism for controlling visibility

### GatedLink Component (NON-NEGOTIABLE)
- EVERY `<Link>` to any dynamic route MUST use `<GatedLink>`
- Check exhaustively: home page, brand index, model listings, sidebar, breadcrumbs, footer links, search results, comparison tool, related items, "see also" sections, sitemap internal links, ANY place a link to a dynamic page exists
- If unpublished: render grey `<span>` with text, no `href`, no click, optional "Próximamente" tooltip
- If published: render normal `<Link>` with full href

### force-dynamic
- ALL listing pages and gate pages: `export const dynamic = 'force-dynamic'`
- Without this, ISR caches 404s for unpublished pages and they NEVER refresh
- This applies to: brand pages (listing models), model pages (listing generations), any page that lists entities

### Sitemap
- Sitemap ONLY includes published pages
- Split by brand: `/sitemap-toyota.xml`, `/sitemap-bmw.xml`, etc.
- Sitemap index at `/sitemap.xml`
- Regenerate on each build/deploy

### Coming Soon UI
- Design this from the START, not retrofit later
- Unpublished entities show: grey/muted card, entity name visible but not clickable
- On direct URL access to unpublished entity: return `notFound()` (real 404)
- The idea is the user sees "oh, Alfa Romeo is coming soon" without hitting errors

### Publication Plan for neumaticopedia.com

**Day 0 (launch):**
- Home page (fully functional)
- Brand index (/marcas) with GatedLink for all brands
- All E-E-A-T pages (about, data sources, contact, privacy, terms, cookies)
- Equivalence calculator (standalone tool, no entity dependency)
- Blog/guides section with 1-2 starter guides
- Header/footer navigation working with GatedLink for unpublished sections
- Everything the home links to must either be live or show Coming Soon gracefully

**Days 1-10: 10-20 pages/day**
- Publish by COMPLETE brand clusters: brand + all its models + generations + variants
- Start with smallest brands first (fewer pages = less risk if something breaks)
- Example: Dacia has ~15 models → publish Dacia brand + all Dacia models/generations/variants in 1-2 days
- Then Seat, Kia, Mazda — brands with 20-40 pages total

**Days 10-20: ramp up to 50 pages/day**
- Move to medium brands: Hyundai, Peugeot, Renault, Ford
- Still complete clusters: never publish a brand page without its models, never a model without its generations

**Days 20+: 50-100 pages/day**
- Big brands: Toyota, BMW, Audi, Mercedes, Volkswagen
- These have hundreds of variants each — publish over several days but always complete one brand before starting the next
- At this point also start publishing tire size pages (/neumaticos/205-55-r16) and PCD pages (/pcd/5x112) as the vehicles linking to them go live

**Ongoing:**
- Tire size and PCD pages only publish when at least 3 vehicles using them are published
- Comparison pages only publish when both vehicles are published
- Pressure guide pages publish alongside their model

**The rule: NEVER publish a parent without its children, NEVER publish a child without its parent. Always complete clusters.**

---

## 2. Pages: noindex, sitemap, and robots

### Pages to INDEX + include in sitemap:
- All published entity pages (brands, models, generations, variants)
- Tire size pages (with published vehicles)
- PCD/bolt pattern pages (with published vehicles)
- Pressure guide pages (with published vehicles)
- Home page
- Brand index (/marcas)
- Blog/guide articles
- Equivalence calculator
- Data Sources page (E-E-A-T!)

### Pages to NOINDEX + exclude from sitemap:
- Privacy Policy
- Terms of Service
- Contact page
- Cookie Policy
- Search results page (/buscar)
- Any filtered/sorted listing variants (query params)
- Comparison tool results (dynamic combos)
- Any page with fewer than 3 published child entities (to avoid thin content perception)

### Pages to block in robots.txt:
- /api/*
- /buscar?* (search with params)
- /_next/* (already default)

---

## 3. E-E-A-T Pages (ALL MANDATORY at launch)

### About (/sobre-nosotros)
- What neumaticopedia.com is: an exhaustive tire/wheel fitment database
- Why it exists: help drivers find the right tire for their car
- How the data is gathered: API sources, cross-referencing methodology
- NOT generic placeholder text

### Data Sources (/fuentes-de-datos) — THE MOST IMPORTANT PAGE
- List EVERY data source with URL
- What data comes from each source
- When data was last updated
- License/attribution if required
- This is what makes Google trust us as E-E-A-T

### Contact (/contacto)
- Contact form (functional!) or email address
- Physical location not required but helpful

### Privacy Policy (/privacidad)
- GDPR compliant
- Mention analytics, cookies, affiliate links
- In Spanish

### Terms of Service (/terminos)
- Standard terms
- Data accuracy disclaimer (measurements are informational, always verify with manufacturer)
- In Spanish

### Cookie Policy (/cookies)
- Required by Spanish LSSI law
- Cookie consent banner on first visit

---

## 4. Technical Checklist (Day 1)

### Branding
- [ ] SVG minimalist logo — tire/wheel-themed, professional, NOT initials
- [ ] Proper favicon (SVG + PNG fallbacks, not just initials)
- [ ] OG image for social sharing (branded, shows what the site is)
- [ ] Consistent color scheme (dark navy + electric blue as per brief)

### Analytics & Tracking
- [ ] Vercel Analytics enabled
- [ ] Vercel Speed Insights enabled
- [ ] Google Analytics 4 (tag ready, Puma will provide ID)
- [ ] Google Search Console verification file/meta tag ready

### Performance
- [ ] No unnecessary npm dependencies
- [ ] Images: next/image with lazy loading, WebP format
- [ ] Fonts: next/font, no external font loading
- [ ] Bundle size: monitor with `next build` output

### Legal Disclaimers
- [ ] Footer: "Los datos de medidas y especificaciones son informativos. Consulte siempre con el fabricante o un profesional."
- [ ] On variant/tire pages: "Las medidas mostradas son orientativas. Verifique la información con el manual de su vehículo."
- [ ] Affiliate disclosure: "Algunos enlaces de esta web son de afiliados. Si compras a través de ellos, podemos recibir una comisión sin coste adicional para ti."

### Infrastructure
- [ ] GitHub repo: `92-neumaticopedia` (under theclankbot org)
- [ ] Vercel project: `92-neumaticopedia`
- [ ] DNS: Puma will register neumaticopedia.com and configure DNS
- [ ] IndexNow: key file in `/public/` for instant indexing on publish

### Deploy Standards
- [ ] Vercel >= 15.3.6
- [ ] Next.js App Router (latest stable)
- [ ] TypeScript
- [ ] Tailwind CSS
- [ ] Static JSON data in `/data/` directory
- [ ] No database — all data pre-computed at build time

---

## 5. Data Quality Rules

- Every data field must have a real value or explicitly show "No disponible" — NEVER empty/blank
- Tire pressure data: if not available from API, do NOT invent it. Show "Consulte el manual del vehículo"
- Cross-reference at minimum: tire sizes + PCD + pressure + basic specs (engine, power, dimensions)
- All numeric data: use Spanish locale formatting (1.234,56 not 1,234.56)
- Dates in Spanish: "1 de abril de 2026"

---

## 6. Things That Will Get You Sent Back by Reviewer

- Any `<Link>` to dynamic routes without GatedLink → instant FIX-REQUIRED
- Missing force-dynamic on listing pages → instant FIX-REQUIRED
- Placeholder text anywhere ("Lorem ipsum", "Coming soon", "TODO") → instant FIX-REQUIRED
- Missing E-E-A-T pages → instant FIX-REQUIRED
- Missing legal disclaimers → instant FIX-REQUIRED
- Console errors → instant FIX-REQUIRED
- Generic/initials favicon → FIX-REQUIRED
- Missing Vercel Analytics → FIX-REQUIRED
- Thin content (page with just a title and 2 numbers) → BLOCK
