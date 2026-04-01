#!/usr/bin/env python3
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "scripts" / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

WIKI_CACHE_PATH = CACHE_DIR / "wikipedia-images.json"
NHTSA_CACHE_PATH = CACHE_DIR / "nhtsa-models.json"
RAW_WHEEL_SIZE_PATH = DATA_DIR / "raw_models_wheelsize.json"

USER_AGENT = "Mozilla/5.0 (compatible; NeumaticopediaBuilder/1.0; +https://neumaticopedia.com)"


def load_json(path, default=None):
    if Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default if default is not None else {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def get_nhtsa_models(make_name, cache):
    key = make_name.lower()
    if key in cache:
        return cache[key]
    encoded = urllib.parse.quote(make_name)
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{encoded}?format=json"
    try:
        payload = fetch_json(url)
        models = sorted({(item.get("Model_Name") or "").strip() for item in payload.get("Results", []) if item.get("Model_Name")})
        cache[key] = {
            "make": make_name,
            "count": len(models),
            "models": models,
            "sourceUrl": url,
            "fetchedAt": time.strftime("%Y-%m-%d"),
        }
    except Exception as exc:
        cache[key] = {
            "make": make_name,
            "count": 0,
            "models": [],
            "sourceUrl": url,
            "fetchedAt": time.strftime("%Y-%m-%d"),
            "error": str(exc),
        }
    time.sleep(0.2)
    return cache[key]


def wikipedia_candidates(brand_name, model_name):
    return [
        f'"{brand_name} {model_name}" car',
        f'"{brand_name} {model_name}" automobile',
        f'"{brand_name} {model_name}"',
        f'{brand_name} {model_name} car',
    ]


def get_wikipedia_image(brand_name, model_name, cache):
    key = f"{brand_name}::{model_name}".lower()
    if key in cache:
        return cache[key]

    result = {
        "imageUrl": None,
        "imagePageUrl": None,
        "imageTitle": None,
        "license": "CC BY-SA / Wikimedia Commons (via Wikipedia page images)",
        "fetchedAt": time.strftime("%Y-%m-%d"),
        "query": None,
    }

    for query in wikipedia_candidates(brand_name, model_name):
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": "1",
            "prop": "pageimages|info",
            "inprop": "url",
            "pithumbsize": "1200",
            "format": "json",
            "origin": "*",
        }
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        try:
            payload = fetch_json(url)
            pages = payload.get("query", {}).get("pages", {})
            if not pages:
                continue
            page = next(iter(pages.values()))
            thumb = page.get("thumbnail", {})
            source = thumb.get("source")
            if source:
                result.update({
                    "imageUrl": source,
                    "imagePageUrl": page.get("fullurl"),
                    "imageTitle": page.get("title"),
                    "query": query,
                })
                break
        except Exception:
            continue
        finally:
            time.sleep(0.1)

    cache[key] = result
    return result


def build_vehicle_finder(brands):
    output = []
    for brand in brands:
        brand_item = {
            "slug": brand["slug"],
            "name": brand["name"],
            "publishedAt": brand.get("publishedAt"),
            "models": [],
        }
        brand_path = DATA_DIR / f"brand-{brand['slug']}.json"
        if not brand_path.exists():
            continue
        full_brand = load_json(brand_path)
        for model in full_brand.get("models", []):
            years = []
            for generation in model.get("generations", []):
                years.append({
                    "slug": generation["slug"],
                    "name": f"{generation['yearStart']}–{generation['yearEnd']}",
                    "publishedAt": generation.get("publishedAt"),
                    "variants": [
                        {
                            "slug": variant["slug"],
                            "name": variant["name"],
                            "publishedAt": variant.get("publishedAt"),
                        }
                        for variant in generation.get("variants", [])
                    ],
                })
            brand_item["models"].append({
                "slug": model["slug"],
                "name": model["name"],
                "publishedAt": model.get("publishedAt"),
                "years": years,
            })
        output.append(brand_item)
    return output


def main():
    brands = load_json(DATA_DIR / "brands.json", [])
    raw_wheel_size = load_json(RAW_WHEEL_SIZE_PATH, {})
    wiki_cache = load_json(WIKI_CACHE_PATH, {})
    nhtsa_cache = load_json(NHTSA_CACHE_PATH, {})
    source_metadata = {
        "generatedAt": time.strftime("%Y-%m-%d"),
        "wheelSize": {},
        "nhtsa": {},
        "wikipedia": {
            "api": "https://en.wikipedia.org/w/api.php",
            "fetchedAt": time.strftime("%Y-%m-%d"),
            "license": "CC BY-SA / Wikimedia Commons",
        },
    }

    image_count = 0

    for brand in brands:
        brand_slug = brand["slug"]
        brand_name = brand["name"]
        brand_file = DATA_DIR / f"brand-{brand_slug}.json"
        if not brand_file.exists():
            continue

        wheel_models = raw_wheel_size.get(brand_slug, {}).get("models", [])
        if not wheel_models and brand_slug == "mercedes-benz":
            wheel_models = raw_wheel_size.get("mercedes", {}).get("models", [])
        source_metadata["wheelSize"][brand_slug] = {
            "brand": brand_name,
            "sourceUrl": f"https://www.wheel-size.com/size/{brand_slug}/",
            "modelCount": len(wheel_models),
            "sampleModels": wheel_models[:12],
            "fetchedAt": time.strftime("%Y-%m-%d"),
            "license": "Datos públicos consultados",
        }

        nhtsa = get_nhtsa_models(brand_name.replace("-Benz", ""), nhtsa_cache)
        source_metadata["nhtsa"][brand_slug] = nhtsa

        brand_data = load_json(brand_file)
        for model in brand_data.get("models", []):
            image = get_wikipedia_image(brand_name, model["name"], wiki_cache)
            model["imageUrl"] = image.get("imageUrl")
            model["imagePageUrl"] = image.get("imagePageUrl")
            model["imageTitle"] = image.get("imageTitle")
            model["imageLicense"] = image.get("license")
            model["imageFetchedAt"] = image.get("fetchedAt")
            model["wheelSizeKnown"] = model["slug"] in wheel_models
            if image.get("imageUrl"):
                image_count += 1

        save_json(brand_file, brand_data)

    save_json(DATA_DIR / "brands.json", brands)
    save_json(DATA_DIR / "vehicle-finder.json", build_vehicle_finder(brands))
    save_json(DATA_DIR / "source-metadata.json", source_metadata)
    save_json(WIKI_CACHE_PATH, wiki_cache)
    save_json(NHTSA_CACHE_PATH, nhtsa_cache)

    print(json.dumps({
        "brands": len(brands),
        "images_found": image_count,
        "vehicle_finder": str(DATA_DIR / 'vehicle-finder.json'),
        "source_metadata": str(DATA_DIR / 'source-metadata.json'),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
