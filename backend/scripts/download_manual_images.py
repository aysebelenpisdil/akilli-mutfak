"""
Downloads recipe images from manually provided URLs.
Edit MANUAL_URLS dict below with  "image_name": "url"  pairs, then run:
    python3 backend/scripts/download_manual_images.py
"""
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
IMG_DIR = ROOT / "public" / "images" / "recipies"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; recipe-image-downloader/1.0)"}

# ── Fill in URLs here ──────────────────────────────────────────────────────────
MANUAL_URLS: dict = {
    # "bayat-pide-kebabi": "https://example.com/image.jpg",
    # "cevizli-kek": "https://...",
}
# ──────────────────────────────────────────────────────────────────────────────


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 5_000:
            print(f"    dosya çok küçük ({len(data)} bytes), atlandı")
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print(f"    hata: {e}")
        return False


def main():
    if not MANUAL_URLS:
        print("MANUAL_URLS boş — scripte URL ekle ve tekrar çalıştır.")
        return

    existing = {f.stem for f in IMG_DIR.iterdir() if f.suffix in (".jpg", ".jpeg")}
    downloaded = 0
    skipped = 0

    for img_name, url in MANUAL_URLS.items():
        if img_name in existing:
            print(f"  ⏭️   zaten var: {img_name}.jpg")
            skipped += 1
            continue

        dest = IMG_DIR / f"{img_name}.jpg"
        print(f"  ⬇️   {img_name}")
        if download(url, dest):
            size_kb = dest.stat().st_size // 1024
            print(f"       ✅  kaydedildi ({size_kb} KB)")
            existing.add(img_name)
            downloaded += 1
        else:
            print(f"       ❌  indirilemedi")

    print(f"\nİndirilen: {downloaded}  |  Atlanan: {skipped}")


if __name__ == "__main__":
    main()
