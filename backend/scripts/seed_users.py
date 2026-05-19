"""
Seed script: 8 gerçekçi fake kullanıcı + tüm ilgili veriler.

Yapılan işlemler:
  1. users tablosuna kullanıcı kaydı
  2. fridge_ingredients
  3. recipe_interactions (like / cook / skip + context_ingredients)
  4. consumption_logs
  5. Supabase Auth'a signup (tarayıcıdan giriş yapabilmek için)

Kullanım:
  cd backend && ./venv/bin/python scripts/seed_users.py

Gereksinimler:
  - Backend .env dosyası yapılandırılmış olmalı (DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY)
  - Supabase Dashboard'da "Confirm email" kapalı olmalı
    (Authentication → Providers → Email → Confirm email: OFF)
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import engine
from sqlalchemy import text

# ─── Sabit şifre ──────────────────────────────────────────────────────────────
PASSWORD = "Test123456"

# ─── Kullanıcı profilleri ──────────────────────────────────────────────────────
# Her kullanıcı için sabit UUID kullanıyoruz (tekrar çalıştırılabilir)
FAKE_USERS = [
    {
        "id": "seed-user-001-ayse-kara-0000000",
        "email": "ayse.kara@test-buzdolabi.com",
        "display_name": "Ayşe Kara",
        "dietary": {},
        "fridge": ["kıyma", "soğan", "domates", "biber", "yoğurt", "sarımsak", "pirinç"],
        "interactions": [
            # (type, recipe_title, context_ingredients)
            ("like",  "Adana Kebap",            ["kıyma", "soğan", "biber"]),
            ("like",  "İçli Köfte",              ["kıyma", "soğan", "bulgur"]),
            ("like",  "Tavuk Şiş",               ["tavuk", "biber", "soğan"]),
            ("like",  "Fırında Tavuk Baget",      ["tavuk", "sarımsak", "limon"]),
            ("like",  "Etli Güveç",               ["et", "domates", "biber"]),
            ("cook",  "Adana Kebap",              ["kıyma", "soğan", "biber"]),
            ("view",  "Ali Nazik Kebap",          ["et", "patlıcan"]),
            ("skip",  "Mercimek Çorbası",         ["mercimek", "soğan"]),
            ("skip",  "Vegan Mercimek Köftesi (Vegan)", ["mercimek", "soğan"]),
        ],
        "consumption": [
            ("Adana Kebap",       "dinner", 1.0, 5),
            ("İçli Köfte",        "lunch",  1.5, 4),
            ("Fırında Tavuk Baget", "dinner", 1.0, 4),
        ],
    },
    {
        "id": "seed-user-002-mehmet-yilmaz-000",
        "email": "mehmet.yilmaz@test-buzdolabi.com",
        "display_name": "Mehmet Yılmaz",
        "dietary": {},
        "fridge": ["tavuk", "kıyma", "soğan", "sarımsak", "biber", "domates", "yağ"],
        "interactions": [
            ("like",  "Adana Kebap",       ["kıyma", "soğan", "biber"]),
            ("like",  "Tavuk Şiş",         ["tavuk", "biber", "soğan"]),
            ("like",  "Tavuk Sote",        ["tavuk", "soğan", "domates"]),
            ("like",  "İskender Kebap",    ["et", "domates salçası", "yoğurt"]),
            ("like",  "Ali Nazik Kebap",   ["et", "patlıcan", "yoğurt"]),
            ("like",  "Tavuk Döner",       ["tavuk", "soğan", "baharatlar"]),
            ("cook",  "Tavuk Sote",        ["tavuk", "soğan", "domates"]),
            ("skip",  "Sütlaç",            ["süt", "pirinç", "şeker"]),
            ("skip",  "Baklava",           ["un", "tereyağı", "şeker"]),
        ],
        "consumption": [
            ("Tavuk Şiş",     "lunch",  1.0, 5),
            ("Tavuk Sote",    "dinner", 1.0, 4),
            ("İskender Kebap", "lunch", 1.0, 5),
        ],
    },
    {
        "id": "seed-user-003-zeynep-demir-000",
        "email": "zeynep.demir@test-buzdolabi.com",
        "display_name": "Zeynep Demir",
        "dietary": {"vegan": True},
        "fridge": ["mercimek", "nohut", "ıspanak", "havuç", "zeytinyağı", "limon", "maydanoz"],
        "interactions": [
            ("like",  "Vegan Mercimek Köftesi (Vegan)",          ["mercimek", "soğan", "maydanoz"]),
            ("like",  "Vegan Yaprak Sarma (Vegan)",              ["zeytinyağı", "pirinç", "limon"]),
            ("like",  "Vegan Mantar Döner (Vegan)",              ["mantar", "soğan", "baharatlar"]),
            ("like",  "Vegan Biber Dolması (Vegan)",             ["biber", "pirinç", "soğan"]),
            ("like",  "Mercimek Çorbası",                         ["mercimek", "soğan", "havuç"]),
            ("cook",  "Vegan Mercimek Köftesi (Vegan)",          ["mercimek", "soğan", "maydanoz"]),
            ("view",  "Ezogelin Çorbası",                         ["mercimek", "bulgur"]),
            ("skip",  "Kuru Fasulye",                             ["fasulye", "et", "soğan"]),
            ("skip",  "Adana Kebap",                              ["kıyma", "soğan", "biber"]),
        ],
        "consumption": [
            ("Vegan Mercimek Köftesi (Vegan)", "lunch",  1.0, 5),
            ("Mercimek Çorbası",               "dinner", 1.0, 4),
            ("Vegan Yaprak Sarma (Vegan)",     "dinner", 1.5, 5),
        ],
    },
    {
        "id": "seed-user-004-canan-sahin-0000",
        "email": "canan.sahin@test-buzdolabi.com",
        "display_name": "Canan Şahin",
        "dietary": {"vegan": True},
        "fridge": ["mercimek", "bulgur", "soğan", "domates", "zeytinyağı", "maydanoz", "limon"],
        "interactions": [
            ("like",  "Vegan Mercimek Köftesi (Vegan)", ["mercimek", "soğan", "maydanoz"]),
            ("like",  "Vegan Biber Dolması (Vegan)",    ["biber", "pirinç", "soğan"]),
            ("like",  "Mercimek Çorbası",                ["mercimek", "soğan", "havuç"]),
            ("like",  "Ezogelin Çorbası",                ["mercimek", "bulgur", "soğan"]),
            ("like",  "Zeytinyağlı Yaprak Sarma",        ["zeytinyağı", "pirinç", "limon"]),
            ("cook",  "Ezogelin Çorbası",                ["mercimek", "bulgur", "soğan"]),
            ("skip",  "Tavuk Şiş",                       ["tavuk", "biber"]),
            ("skip",  "Etli Güveç",                      ["et", "domates"]),
        ],
        "consumption": [
            ("Ezogelin Çorbası",                "lunch",  1.0, 5),
            ("Vegan Biber Dolması (Vegan)",     "dinner", 1.0, 4),
            ("Zeytinyağlı Yaprak Sarma",        "lunch",  1.0, 5),
        ],
    },
    {
        "id": "seed-user-005-emre-arslan-0000",
        "email": "emre.arslan@test-buzdolabi.com",
        "display_name": "Emre Arslan",
        "dietary": {},
        "fridge": ["kuru fasulye", "pirinç", "salça", "soğan", "domates", "et", "sarımsak"],
        "interactions": [
            ("like",  "Kuru Fasulye",              ["kuru fasulye", "soğan", "salça"]),
            ("like",  "Pilav Üstü Kuru Fasulye",   ["kuru fasulye", "pirinç", "soğan"]),
            ("like",  "Mercimek Çorbası",           ["mercimek", "soğan", "havuç"]),
            ("like",  "Etli Nohut Yemeği",          ["nohut", "et", "soğan"]),
            ("like",  "Bulgur Pilavı",              ["bulgur", "soğan", "salça"]),
            ("like",  "Tereyağlı Pirinç Pilavı",    ["pirinç", "tereyağı", "tuz"]),
            ("cook",  "Kuru Fasulye",              ["kuru fasulye", "soğan", "salça"]),
            ("cook",  "Etli Nohut Yemeği",          ["nohut", "et", "soğan"]),
            ("view",  "Nohutlu Pirinç Pilavı",      ["nohut", "pirinç"]),
        ],
        "consumption": [
            ("Kuru Fasulye",            "lunch",  1.0, 5),
            ("Etli Nohut Yemeği",       "dinner", 1.0, 5),
            ("Tereyağlı Pirinç Pilavı", "dinner", 1.0, 4),
        ],
    },
    {
        "id": "seed-user-006-fatma-celik-0000",
        "email": "fatma.celik@test-buzdolabi.com",
        "display_name": "Fatma Çelik",
        "dietary": {},
        "fridge": ["kuru fasulye", "nohut", "pirinç", "domates", "soğan", "salça", "et"],
        "interactions": [
            ("like",  "Kuru Fasulye",             ["kuru fasulye", "soğan", "salça"]),
            ("like",  "Etli Nohut Yemeği",         ["nohut", "et", "soğan"]),
            ("like",  "Ezogelin Çorbası",           ["mercimek", "bulgur", "soğan"]),
            ("like",  "Zeytinyağlı Yaprak Sarma",   ["zeytinyağı", "pirinç", "limon"]),
            ("like",  "Nohutlu Pirinç Pilavı",      ["nohut", "pirinç", "soğan"]),
            ("like",  "Tavuklu Pilav",              ["tavuk", "pirinç", "baharatlar"]),
            ("cook",  "Etli Nohut Yemeği",          ["nohut", "et", "soğan"]),
            ("cook",  "Kuru Fasulye",               ["kuru fasulye", "soğan", "salça"]),
            ("skip",  "Baklava",                    ["un", "şeker", "tereyağı"]),
        ],
        "consumption": [
            ("Etli Nohut Yemeği",      "dinner", 1.0, 5),
            ("Kuru Fasulye",           "lunch",  1.0, 5),
            ("Nohutlu Pirinç Pilavı",  "dinner", 1.5, 4),
        ],
    },
    {
        "id": "seed-user-007-burak-ozdemir-00",
        "email": "burak.ozdemir@test-buzdolabi.com",
        "display_name": "Burak Özdemir",
        "dietary": {},
        "fridge": ["balık fileto", "limon", "zeytinyağı", "maydanoz", "sarımsak", "tuz", "karabiber"],
        "interactions": [
            ("like",  "Balık Buğulama",   ["balık fileto", "limon", "zeytinyağı"]),
            ("like",  "Balık Köfte",      ["balık", "soğan", "maydanoz"]),
            ("like",  "Midye Dolma",      ["midye", "pirinç", "baharatlar"]),
            ("like",  "Patlıcan Salatası",["patlıcan", "zeytinyağı", "limon"]),
            ("like",  "Çoban Salatası",   ["domates", "salatalık", "soğan"]),
            ("cook",  "Balık Buğulama",   ["balık fileto", "limon", "zeytinyağı"]),
            ("view",  "Midye Dolma",      ["midye", "pirinç"]),
            ("skip",  "Baklava",          ["un", "şeker", "tereyağı"]),
        ],
        "consumption": [
            ("Balık Buğulama",  "dinner", 1.0, 5),
            ("Midye Dolma",     "lunch",  1.0, 4),
            ("Çoban Salatası",  "lunch",  1.0, 4),
        ],
    },
    {
        "id": "seed-user-008-selin-aydin-0000",
        "email": "selin.aydin@test-buzdolabi.com",
        "display_name": "Selin Aydın",
        "dietary": {},
        "fridge": ["un", "yumurta", "tereyağı", "süt", "şeker", "tuz", "peynir"],
        "interactions": [
            ("like",  "Baklava",            ["un", "tereyağı", "şeker"]),
            ("like",  "Sütlaç",             ["süt", "pirinç", "şeker"]),
            ("like",  "Fırında Sütlaç",     ["süt", "pirinç", "şeker"]),
            ("like",  "Peynirli Gözleme",   ["un", "peynir", "tereyağı"]),
            ("like",  "Peynirli Poğaça",    ["un", "peynir", "yumurta"]),
            ("like",  "Ispanaklı Börek",    ["un", "ıspanak", "peynir"]),
            ("cook",  "Baklava",            ["un", "tereyağı", "şeker"]),
            ("cook",  "Sütlaç",             ["süt", "pirinç", "şeker"]),
            ("skip",  "Adana Kebap",        ["kıyma", "soğan"]),
        ],
        "consumption": [
            ("Baklava",           "snack",  1.0, 5),
            ("Sütlaç",            "snack",  1.5, 5),
            ("Peynirli Gözleme",  "breakfast", 1.0, 4),
        ],
    },
]


# ─── DB işlemleri ─────────────────────────────────────────────────────────────

async def insert_user(conn, user: dict) -> None:
    dietary_json = json.dumps(user["dietary"], ensure_ascii=False)
    await conn.execute(
        text("""
            INSERT INTO users (id, email, display_name, dietary_preferences, created_at)
            VALUES (:id, :email, :display_name, :dietary, NOW())
            ON CONFLICT (email) DO UPDATE SET
                display_name = EXCLUDED.display_name,
                dietary_preferences = EXCLUDED.dietary_preferences
        """),
        {
            "id": user["id"],
            "email": user["email"],
            "display_name": user["display_name"],
            "dietary": dietary_json,
        },
    )


async def insert_fridge(conn, user: dict) -> None:
    await conn.execute(
        text("DELETE FROM fridge_ingredients WHERE user_id = :uid"),
        {"uid": user["id"]},
    )
    for ing in user["fridge"]:
        await conn.execute(
            text("""
                INSERT INTO fridge_ingredients (user_id, ingredient)
                VALUES (:uid, :ing) ON CONFLICT DO NOTHING
            """),
            {"uid": user["id"], "ing": ing},
        )


async def insert_interactions(conn, user: dict) -> None:
    # Eski seed verisini temizle
    await conn.execute(
        text("DELETE FROM recipe_interactions WHERE user_id = :uid"),
        {"uid": user["id"]},
    )
    base_date = datetime.utcnow() - timedelta(days=30)
    for i, (itype, title, ctx_ingredients) in enumerate(user["interactions"]):
        created_at = base_date + timedelta(days=i * 2, hours=i)
        await conn.execute(
            text("""
                INSERT INTO recipe_interactions
                    (user_id, recipe_title, interaction_type, context_ingredients, created_at)
                VALUES (:uid, :title, :itype, :ctx, :created_at)
                ON CONFLICT (user_id, recipe_title, interaction_type)
                    WHERE interaction_type IN ('like','skip','save','cook')
                    DO UPDATE SET
                        context_ingredients = EXCLUDED.context_ingredients,
                        created_at = EXCLUDED.created_at
            """),
            {
                "uid": user["id"],
                "title": title,
                "itype": itype,
                "ctx": json.dumps(ctx_ingredients, ensure_ascii=False),
                "created_at": created_at,
            },
        )


async def insert_consumption(conn, user: dict) -> None:
    await conn.execute(
        text("DELETE FROM consumption_logs WHERE user_id = :uid"),
        {"uid": user["id"]},
    )
    base_date = datetime.utcnow() - timedelta(days=20)
    for i, (title, meal_type, portion, rating) in enumerate(user["consumption"]):
        consumed_at = base_date + timedelta(days=i * 3)
        await conn.execute(
            text("""
                INSERT INTO consumption_logs
                    (user_id, recipe_title, meal_type, portion_size, rating, consumed_at)
                VALUES (:uid, :title, :meal, :portion, :rating, :consumed_at)
            """),
            {
                "uid": user["id"],
                "title": title,
                "meal": meal_type,
                "portion": portion,
                "rating": rating,
                "consumed_at": consumed_at,
            },
        )


async def seed_db() -> None:
    print("\n📦 Veritabanına seed verisi ekleniyor...\n")
    async with engine.begin() as conn:
        for user in FAKE_USERS:
            await insert_user(conn, user)
            await insert_fridge(conn, user)
            await insert_interactions(conn, user)
            await insert_consumption(conn, user)
            print(f"  ✓ {user['display_name']} ({user['email']})")
    print(f"\n  Toplam {len(FAKE_USERS)} kullanıcı eklendi.\n")


# ─── Supabase Auth kaydı ───────────────────────────────────────────────────────

async def signup_supabase(email: str, password: str, client: httpx.AsyncClient) -> str:
    """
    Kullanıcıyı Supabase Auth'a kaydet.
    Döner: 'ok' | 'already_exists' | 'needs_confirmation' | 'error:<msg>'
    """
    resp = await client.post(
        f"{settings.SUPABASE_URL}/auth/v1/signup",
        headers={
            "apikey": settings.SUPABASE_ANON_KEY,
            "Content-Type": "application/json",
        },
        json={"email": email, "password": password},
        timeout=15,
    )

    if resp.status_code in (200, 201):
        data = resp.json()
        # Email confirmation kapalıysa session hemen gelir
        if data.get("access_token") or (data.get("session") and data["session"]):
            return "ok"
        # Email confirmation açıksa session gelmez
        if data.get("user") and not data.get("access_token"):
            return "needs_confirmation"
        return "ok"

    body = resp.json()
    msg = body.get("msg") or body.get("message") or body.get("error_description") or str(body)

    if "already registered" in msg.lower() or resp.status_code == 422:
        return "already_exists"

    return f"error:{resp.status_code} {msg}"


async def seed_supabase() -> None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        print("⚠️  SUPABASE_URL veya SUPABASE_ANON_KEY eksik — Supabase adımı atlandı.")
        return

    print("🔐 Supabase Auth'a kullanıcılar kaydediliyor...\n")
    needs_confirm: list[str] = []
    errors: list[str] = []

    async with httpx.AsyncClient() as client:
        for user in FAKE_USERS:
            result = await signup_supabase(user["email"], PASSWORD, client)
            if result == "ok":
                print(f"  ✓ {user['email']}")
            elif result == "already_exists":
                print(f"  ℹ  {user['email']} — zaten kayıtlı, atlandı")
            elif result == "needs_confirmation":
                print(f"  ⚠  {user['email']} — email onayı gerekiyor")
                needs_confirm.append(user["email"])
            else:
                print(f"  ✗ {user['email']} — {result}")
                errors.append(user["email"])

    if needs_confirm:
        print(
            "\n⚠️  Email onayı gerekiyor!\n"
            "   Supabase Dashboard → Authentication → Providers → Email\n"
            "   'Confirm email' seçeneğini KAPATIN, sonra scripti tekrar çalıştırın.\n"
        )
    if errors:
        print(f"\n✗ Başarısız kullanıcılar: {errors}\n")


# ─── Ana akış ─────────────────────────────────────────────────────────────────

async def main() -> None:
    await seed_db()
    await seed_supabase()

    print("=" * 60)
    print("GİRİŞ BİLGİLERİ (hepsi aynı şifre)")
    print("=" * 60)
    for u in FAKE_USERS:
        print(f"  {u['display_name']:<20} {u['email']}")
    print(f"\n  Şifre: {PASSWORD}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    asyncio.run(main())
