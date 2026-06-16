"""
Downloads missing recipe images using DuckDuckGo image search.
Run from project root: python backend/scripts/download_recipe_images.py

Requires: pip install duckduckgo-search
"""
import json
import time
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_JSON = ROOT / "backend" / "data" / "recipes.json"
IMG_DIR = ROOT / "public" / "images" / "recipies"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; recipe-image-downloader/1.0)"}

TITLE_SUFFIXES = [
    " (Vegan)", " (Vejetaryen)", " (Glutensiz)", " (Süt Ürünü Yok)",
    " (Glutensiz & Vejetaryen)", " (Vegan & Glutensiz)", " (Laktozsuz)",
    " (Kuruyemiş İçermez)",
]

PREFIXES = [
    "vegan-", "glutensiz-", "sut-urunsuz-", "vejetaryen-",
    "laktozsuz-", "kuruyemissiz-",
]


def clean_title(title: str) -> str:
    for s in TITLE_SUFFIXES:
        title = title.replace(s, "")
    return title.strip()


def base_title(title: str) -> str:
    """Strip dietary prefix words from title for a cleaner search query."""
    return re.sub(r"^(Vegan|Vejetaryen|Glutensiz|Süt Ürünsüz|Laktozsuz|Kuruyemissiz)\s+", "", title, flags=re.I).strip()


def search_image_url(ddgs, query: str):
    """Search using an existing DDGS instance (shared across all calls)."""
    for attempt in range(3):
        try:
            results = list(ddgs.images(query, max_results=3))
            for r in results:
                url = r.get("image", "")
                if url and url.lower().endswith((".jpg", ".jpeg")):
                    return url
            for r in results:
                url = r.get("image", "")
                if url:
                    return url
            return None
        except Exception as e:
            msg = str(e)
            if "403" in msg or "Ratelimit" in msg:
                wait = 10 * (attempt + 1)
                print(f"    rate limit, {wait}s bekleniyor...")
                time.sleep(wait)
            else:
                print(f"    DDG error: {e}")
                return None
    return None


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 5_000:
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print(f"    download error: {e}")
        return False


def _find_missing_recipes(data: list, existing: set) -> list:
    """Return list of (img_name, cleaned_title) for recipes without a local image."""
    missing = []
    for recipe in data:
        img_name = recipe.get("Image_Name", "")
        if img_name and f"{img_name}.jpg" not in existing:
            missing.append((img_name, clean_title(recipe.get("Title", ""))))
    return missing


def _search_first_url(ddgs, title: str) -> str | None:
    """Try multiple query variants and return the first successful image URL."""
    short = base_title(title)
    for query in [f"{short} tarifi", f"{short} yemek", short]:
        url = search_image_url(ddgs, query)
        if url:
            return url
        time.sleep(2.0)
    return None


def _process_recipe(ddgs, img_name: str, title: str, existing: set) -> bool:
    """Download image for one recipe. Returns True if downloaded successfully."""
    dest = IMG_DIR / f"{img_name}.jpg"
    url = _search_first_url(ddgs, title)
    if url and download(url, dest):
        size_kb = dest.stat().st_size // 1024
        print(f"         ✅  kaydedildi ({size_kb} KB)")
        existing.add(dest.name)
        return True
    print(f"         ❌  bulunamadı")
    return False


def _import_ddgs():
    """Import DDGS from whichever package is installed, or return None."""
    try:
        from ddgs import DDGS
        return DDGS
    except ImportError:
        pass
    try:
        from duckduckgo_search import DDGS
        return DDGS
    except ImportError:
        return None


def main():
    DDGS = _import_ddgs()
    if DDGS is None:
        print("Hata: ddgs kurulu değil.")
        print("Çalıştır: pip3 install ddgs")
        return

    data = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
    existing = {f.name for f in IMG_DIR.iterdir() if f.suffix in (".jpg", ".jpeg")}
    missing = _find_missing_recipes(data, existing)

    print(f"İndirilecek görsel: {len(missing)}\n")

    downloaded = 0
    not_found = []
    ddgs = DDGS()

    for i, (img_name, title) in enumerate(missing, 1):
        print(f"[{i:3}/{len(missing)}] {title}")
        if _process_recipe(ddgs, img_name, title, existing):
            downloaded += 1
        else:
            not_found.append(img_name)
        time.sleep(3.0)

    print(f"\n{'='*50}")
    print(f"✅  İndirilen : {downloaded}")
    print(f"❌  Bulunamayan: {len(not_found)}")
    if not_found:
        print("Bulunamayan görseller:")
        for n in not_found:
            print(f"  {n}")


if __name__ == "__main__":
    main()
