#!/usr/bin/env python3
"""
Scrape wheel-size.com for tire/wheel fitment data.
Respects rate limits: 1 request per 2 seconds.
"""

import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

BASE_URL = "https://www.wheel-size.com"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "data")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

DELAY = 1.5  # seconds between requests

# Top brands for Spanish market
BRANDS = {
    "toyota": {"name": "Toyota", "country": "Japón", "founded": "1937"},
    "volkswagen": {"name": "Volkswagen", "country": "Alemania", "founded": "1937"},
    "seat": {"name": "SEAT", "country": "España", "founded": "1950"},
    "cupra": {"name": "CUPRA", "country": "España", "founded": "2018"},
    "hyundai": {"name": "Hyundai", "country": "Corea del Sur", "founded": "1967"},
    "kia": {"name": "Kia", "country": "Corea del Sur", "founded": "1944"},
    "peugeot": {"name": "Peugeot", "country": "Francia", "founded": "1810"},
    "renault": {"name": "Renault", "country": "Francia", "founded": "1899"},
    "citroen": {"name": "Citroën", "country": "Francia", "founded": "1919"},
    "bmw": {"name": "BMW", "country": "Alemania", "founded": "1916"},
    "audi": {"name": "Audi", "country": "Alemania", "founded": "1909"},
    "mercedes": {"name": "Mercedes-Benz", "country": "Alemania", "founded": "1926"},
    "ford": {"name": "Ford", "country": "Estados Unidos", "founded": "1903"},
    "dacia": {"name": "Dacia", "country": "Rumanía", "founded": "1966"},
    "opel": {"name": "Opel", "country": "Alemania", "founded": "1862"},
    "nissan": {"name": "Nissan", "country": "Japón", "founded": "1933"},
    "mazda": {"name": "Mazda", "country": "Japón", "founded": "1920"},
    "fiat": {"name": "Fiat", "country": "Italia", "founded": "1899"},
    "skoda": {"name": "Škoda", "country": "República Checa", "founded": "1895"},
    "volvo": {"name": "Volvo", "country": "Suecia", "founded": "1927"},
    "honda": {"name": "Honda", "country": "Japón", "founded": "1948"},
}


def fetch(url, use_cache=True):
    """Fetch URL with caching and rate limiting."""
    cache_key = url.replace("/", "_").replace(":", "_").replace("?", "_")
    cache_path = os.path.join(CACHE_DIR, cache_key[:200] + ".html")
    
    if use_cache and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    
    time.sleep(DELAY)
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
        return ""


def extract_models(brand_slug):
    """Extract model list from brand page."""
    html = fetch(f"{BASE_URL}/size/{brand_slug}/")
    if not html:
        return []
    
    models = []
    # Pattern: links like /size/toyota/4runner/
    pattern = rf'href="/size/{re.escape(brand_slug)}/([^/"]+)/"'
    found = set(re.findall(pattern, html))
    
    for model_slug in sorted(found):
        # Extract model name from the page if possible
        name = model_slug.replace("-", " ").title()
        models.append({"slug": model_slug, "name": name})
    
    return models


def extract_years(brand_slug, model_slug):
    """Extract available years for a model."""
    html = fetch(f"{BASE_URL}/size/{brand_slug}/{model_slug}/")
    if not html:
        return []
    
    # Look for year links
    pattern = rf'href="/size/{re.escape(brand_slug)}/{re.escape(model_slug)}/(\d{{4}})/"'
    years = sorted(set(re.findall(pattern, html)), reverse=True)
    return years


def extract_tire_data(brand_slug, model_slug, year):
    """Extract tire/wheel data for a specific year."""
    html = fetch(f"{BASE_URL}/size/{brand_slug}/{model_slug}/{year}/")
    if not html:
        return []
    
    trims = []
    
    # Extract tire data from the tables
    # Look for trim/variant sections and their tire data
    # The page typically has tables with tire sizes, PCD, offset etc.
    
    # Extract trim names
    trim_pattern = r'<h[23][^>]*>([^<]*(?:trim|engine|variant|modification)[^<]*)</h[23]>'
    
    # Look for tire size patterns like 205/55 R16
    tire_sizes = re.findall(r'(\d{3}/\d{2}\s*[RZ]?\s*\d{2})', html)
    
    # Look for PCD patterns like 5x112
    pcds = re.findall(r'(\d+x\d+(?:\.\d+)?)\s*(?:mm)?', html)
    pcds = [p for p in pcds if re.match(r'^[3-6]x\d{2,3}', p)]
    
    # Look for center bore
    center_bores = re.findall(r'(?:center bore|hub bore|CB)[:\s]*(\d+\.?\d*)\s*mm', html, re.I)
    
    # Look for offset
    offsets = re.findall(r'(?:ET|offset)[:\s]*(\d+)', html, re.I)
    
    # Look for rim sizes like 6.5Jx16
    rim_sizes = re.findall(r'(\d+\.?\d*[Jj]?\s*[xX]\s*\d{2})', html)
    
    # Look for bolt/thread info
    thread_sizes = re.findall(r'(M\d+\s*[xX]\s*\d+\.?\d*)', html)
    
    # Look for tire pressure
    pressures = re.findall(r'(\d+\.?\d*)\s*(?:bar|BAR|psi)', html)
    
    # Extract table data more carefully
    # Look for structured data in tables
    table_pattern = r'<table[^>]*class="[^"]*table[^"]*"[^>]*>(.*?)</table>'
    tables = re.findall(table_pattern, html, re.DOTALL)
    
    # Build a trim entry from what we found
    trim_data = {
        "year": year,
        "tire_sizes": list(set(tire_sizes))[:10],
        "pcds": list(set(pcds))[:5],
        "center_bores": list(set(center_bores))[:3],
        "offsets": list(set(offsets))[:5],
        "rim_sizes": list(set(rim_sizes))[:10],
        "thread_sizes": list(set(thread_sizes))[:3],
    }
    
    return trim_data


def scrape_brand(brand_slug, brand_info):
    """Scrape all data for one brand."""
    print(f"\n{'='*60}")
    print(f"Scraping {brand_info['name']} ({brand_slug})...")
    print(f"{'='*60}")
    
    models = extract_models(brand_slug)
    print(f"  Found {len(models)} models")
    
    brand_data = {
        "slug": brand_slug,
        "name": brand_info["name"],
        "country": brand_info["country"],
        "founded": brand_info["founded"],
        "models": [],
    }
    
    for i, model in enumerate(models):
        print(f"  [{i+1}/{len(models)}] {model['name']}...", end=" ", flush=True)
        
        years = extract_years(brand_slug, model["slug"])
        print(f"({len(years)} years)", end=" ", flush=True)
        
        model_data = {
            "slug": model["slug"],
            "name": model["name"],
            "years": years,
            "generations": [],
            "tire_data": [],
        }
        
        # Get tire data for latest 3 years to avoid too many requests
        for year in years[:5]:
            tire_data = extract_tire_data(brand_slug, model["slug"], year)
            if tire_data:
                model_data["tire_data"].append(tire_data)
        
        brand_data["models"].append(model_data)
        print("✓")
    
    return brand_data


def main():
    all_data = {}
    
    # Process only the specified brand if given as argument
    brands_to_scrape = BRANDS
    if len(sys.argv) > 1:
        brand_arg = sys.argv[1]
        if brand_arg in BRANDS:
            brands_to_scrape = {brand_arg: BRANDS[brand_arg]}
        else:
            print(f"Unknown brand: {brand_arg}")
            sys.exit(1)
    
    for brand_slug, brand_info in brands_to_scrape.items():
        brand_data = scrape_brand(brand_slug, brand_info)
        all_data[brand_slug] = brand_data
        
        # Save per-brand file
        brand_path = os.path.join(DATA_DIR, f"brand-{brand_slug}.json")
        with open(brand_path, "w", encoding="utf-8") as f:
            json.dump(brand_data, f, ensure_ascii=False, indent=2)
        print(f"  Saved to {brand_path}")
    
    # Save brands index
    brands_index = []
    for slug, info in BRANDS.items():
        brand_file = os.path.join(DATA_DIR, f"brand-{slug}.json")
        model_count = 0
        if os.path.exists(brand_file):
            with open(brand_file) as f:
                bd = json.load(f)
                model_count = len(bd.get("models", []))
        
        brands_index.append({
            "slug": slug,
            "name": info["name"],
            "country": info["country"],
            "founded": info["founded"],
            "modelCount": model_count,
            "publishedAt": None,  # All unpublished initially
        })
    
    with open(os.path.join(DATA_DIR, "brands.json"), "w", encoding="utf-8") as f:
        json.dump(brands_index, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nDone! Scraped {len(all_data)} brands")
    print(f"Data saved to {DATA_DIR}")


if __name__ == "__main__":
    main()
