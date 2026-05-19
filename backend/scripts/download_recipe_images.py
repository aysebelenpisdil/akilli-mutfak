"""
Downloads missing recipe images from Wikimedia Commons.
Run from project root: python backend/scripts/download_recipe_images.py

Uses only stdlib — no extra dependencies needed.
Rate-limited to be polite to Wikimedia servers (1 req/sec).
"""
import json
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_JSON = ROOT / "backend" / "data" / "recipes.json"
IMG_DIR = ROOT / "public" / "images" / "recipies"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "RecipeImageBot/1.0 (academic graduation project; urllib)"}

PREFIXES = [
    "vegan-", "glutensiz-", "sut-urunsuz-", "vejetaryen-",
    "laktozsuz-", "kuruyemissiz-",
]

TITLE_SUFFIXES = [
    " (Vegan)", " (Vejetaryen)", " (Glutensiz)", " (Süt Ürünü Yok)",
    " (Glutensiz & Vejetaryen)", " (Vegan & Glutensiz)", " (Laktozsuz)",
    " (Kuruyemiş İçermez)",
]


def clean_title(title: str) -> str:
    for s in TITLE_SUFFIXES:
        title = title.replace(s, "")
    return title.strip()


def _api_get(params: dict, retries: int = 3) -> dict:
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 5 * (attempt + 1)
                print(f"    429 rate limit, {wait}s bekleniyor...")
                time.sleep(wait)
            else:
                raise
    return {}


def search_files(query: str) -> list[str]:
    """Return up to 5 Wikimedia Commons file titles matching the query."""
    try:
        data = _api_get({
            "action": "query", "format": "json",
            "list": "search",
            "srsearch": query,
            "srnamespace": "6",
            "srlimit": "5",
            "utf8": "1",
        })
        return [item["title"] for item in data.get("query", {}).get("search", [])]
    except Exception as e:
        print(f"    search error: {e}")
        return []


def get_jpeg_url(file_title: str):
    """Return a ~800px-wide JPEG URL for a Commons file, or None if not JPEG."""
    try:
        data = _api_get({
            "action": "query", "format": "json",
            "titles": file_title,
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": "800",
        })
        for page in data.get("query", {}).get("pages", {}).values():
            for info in page.get("imageinfo", []):
                mime = info.get("mime", "")
                if "jpeg" in mime or "jpg" in mime:
                    return info.get("thumburl") or info.get("url")
    except Exception as e:
        print(f"    imageinfo error: {e}")
    return None


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            dest.write_bytes(r.read())
        return dest.stat().st_size > 5_000  # reject tiny/broken files
    except Exception as e:
        print(f"    download error: {e}")
        return False


def find_image(title: str):
    """Try several search queries for a recipe title, return JPEG URL or None."""
    queries = [
        title,
        f"{title} yemeği",
        f"{title} Turkish food",
        # ASCII fallback: replace Turkish chars
        re.sub(r"[ğĞ]", "g", re.sub(r"[üÜ]", "u",
               re.sub(r"[şŞ]", "s", re.sub(r"[ıİ]", "i",
               re.sub(r"[öÖ]", "o", re.sub(r"[çÇ]", "c", title)))))),
    ]
    for q in queries:
        for file_title in search_files(q):
            url = get_jpeg_url(file_title)
            if url:
                return url
        time.sleep(2.0)
    return None


def main():
    data = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
    existing = {f.name for f in IMG_DIR.iterdir() if f.suffix == ".jpg"}

    # Build (img_name, clean_title) list for all still-missing images
    missing = []
    for recipe in data:
        img_name = recipe.get("Image_Name", "")
        if not img_name or f"{img_name}.jpg" in existing:
            continue
        title = clean_title(recipe.get("Title", ""))
        missing.append((img_name, title))

    print(f"İndirilecek görsel: {len(missing)}\n")

    downloaded = 0
    not_found = []

    for i, (img_name, title) in enumerate(missing, 1):
        dest = IMG_DIR / f"{img_name}.jpg"
        print(f"[{i:3}/{len(missing)}] {title}")

        url = find_image(title)
        if url and download(url, dest):
            size_kb = dest.stat().st_size // 1024
            print(f"         ✅  kaydedildi ({size_kb} KB)")
            existing.add(dest.name)
            downloaded += 1
        else:
            print(f"         ❌  bulunamadı")
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
