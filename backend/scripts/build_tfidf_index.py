import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.recipe_service import recipe_service
from app.services.tfidf_service import tfidf_service


def main():
    recipe_service._load_recipes()
    recipes = recipe_service.recipes
    if not recipes:
        print("Tarif yüklenemedi")
        return
    print(f"{len(recipes)} tarif için TF-IDF indeksi oluşturuluyor...")
    tfidf_service.build_index(recipes)
    print(
        f"Tamam. Matris: {tfidf_service._matrix.shape}, "
        f"vocab: {tfidf_service.vocab_size}"
    )


if __name__ == "__main__":
    main()
