"""
Copies base recipe images to dietary variant filenames.
e.g.  cilbir.jpg  →  vegan-cilbir.jpg
Run from project root: python backend/scripts/copy_variant_images.py
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RECIPES_JSON = ROOT / "backend" / "data" / "recipes.json"
IMG_DIR = ROOT / "public" / "images" / "recipies"

PREFIXES = [
    "vegan-", "glutensiz-", "sut-urunsuz-", "vejetaryen-",
    "laktozsuz-", "kuruyemissiz-",
]


def main():
    data = json.loads(RECIPES_JSON.read_text(encoding="utf-8"))
    existing = {f.name for f in IMG_DIR.iterdir() if f.suffix == ".jpg"}

    copied = 0
    base_missing = []

    for recipe in data:
        img_name = recipe.get("Image_Name", "")
        if not img_name:
            continue

        target = f"{img_name}.jpg"
        if target in existing:
            continue

        for prefix in PREFIXES:
            if img_name.startswith(prefix):
                base = f"{img_name[len(prefix):]}.jpg"
                if base in existing:
                    shutil.copy2(IMG_DIR / base, IMG_DIR / target)
                    existing.add(target)
                    copied += 1
                    print(f"  ✅  {base}  →  {target}")
                else:
                    base_missing.append((img_name, base))
                break

    print(f"\nKopyalanan: {copied}")
    print(f"Base görseli de yok: {len(base_missing)}")


if __name__ == "__main__":
    main()
