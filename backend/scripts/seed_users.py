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
import os as _os
PASSWORD = _os.getenv("SEED_USER_PASSWORD")
if not PASSWORD:
    raise RuntimeError("SEED_USER_PASSWORD environment variable must be set")

# ─── Tekrarlayan sabit dizeler ────────────────────────────────────────────────
# Ingredients
ING_SOGHAN = "soğan"
ING_PIRINC = "pirinç"
ING_KIYMA = "kıyma"
ING_TEREYAGI = "tereyağı"
ING_SEKER = "şeker"
ING_ZEYTINYAGI = "zeytinyağı"
ING_SARIMSAK = "sarımsak"
ING_HAVUC = "havuç"
ING_YOGURT = "yoğurt"
ING_PATLICAN = "patlıcan"
ING_KURU_FASULYE = "kuru fasulye"
ING_SALCA = "salça"
ING_BALIK_FILETO = "balık fileto"

# Recipe titles
RCP_ADANA_KEBAP = "Adana Kebap"
RCP_TAVUK_SIS = "Tavuk Şiş"
RCP_MERCIMEK_CORBASI = "Mercimek Çorbası"
RCP_VEGAN_MERCIMEK = "Vegan Mercimek Köftesi (Vegan)"
RCP_TAVUK_SOTE = "Tavuk Sote"
RCP_SUTLAC = "Sütlaç"
RCP_VEGAN_BIBER_DOLMASI = "Vegan Biber Dolması (Vegan)"
RCP_EZOGELIN_CORBASI = "Ezogelin Çorbası"
RCP_KURU_FASULYE = "Kuru Fasulye"
RCP_ZEYTINYAGLI_YAPRAK_SARMA = "Zeytinyağlı Yaprak Sarma"
RCP_ETLI_NOHUT = "Etli Nohut Yemeği"
RCP_NOHUTLU_PIRINC = "Nohutlu Pirinç Pilavı"
RCP_BALIK_BUGULAMA = "Balık Buğulama"
RCP_MIDYE_DOLMA = "Midye Dolma"

# ─── Kullanıcı profilleri ──────────────────────────────────────────────────────
# Her kullanıcı için sabit UUID kullanıyoruz (tekrar çalıştırılabilir)
FAKE_USERS = [
    {
        "id": "seed-user-001-ayse-kara-0000000",
        "email": "ayse.kara@test-buzdolabi.com",
        "display_name": "Ayşe Kara",
        "dietary": {},
        "fridge": [ING_KIYMA, ING_SOGHAN, "domates", "biber", ING_YOGURT, ING_SARIMSAK, ING_PIRINC],
        "interactions": [
            # (type, recipe_title, context_ingredients)
            ("like",  RCP_ADANA_KEBAP,            [ING_KIYMA, ING_SOGHAN, "biber"]),
            ("like",  "İçli Köfte",              [ING_KIYMA, ING_SOGHAN, "bulgur"]),
            ("like",  RCP_TAVUK_SIS,               ["tavuk", "biber", ING_SOGHAN]),
            ("like",  "Fırında Tavuk Baget",      ["tavuk", ING_SARIMSAK, "limon"]),
            ("like",  "Etli Güveç",               ["et", "domates", "biber"]),
            ("cook",  RCP_ADANA_KEBAP,              [ING_KIYMA, ING_SOGHAN, "biber"]),
            ("view",  "Ali Nazik Kebap",          ["et", ING_PATLICAN]),
            ("skip",  RCP_MERCIMEK_CORBASI,         ["mercimek", ING_SOGHAN]),
            ("skip",  RCP_VEGAN_MERCIMEK, ["mercimek", ING_SOGHAN]),
        ],
        "consumption": [
            (RCP_ADANA_KEBAP,       "dinner", 1.0, 5),
            ("İçli Köfte",        "lunch",  1.5, 4),
            ("Fırında Tavuk Baget", "dinner", 1.0, 4),
        ],
    },
    {
        "id": "seed-user-002-mehmet-yilmaz-000",
        "email": "mehmet.yilmaz@test-buzdolabi.com",
        "display_name": "Mehmet Yılmaz",
        "dietary": {},
        "fridge": ["tavuk", ING_KIYMA, ING_SOGHAN, ING_SARIMSAK, "biber", "domates", "yağ"],
        "interactions": [
            ("like",  RCP_ADANA_KEBAP,       [ING_KIYMA, ING_SOGHAN, "biber"]),
            ("like",  RCP_TAVUK_SIS,         ["tavuk", "biber", ING_SOGHAN]),
            ("like",  RCP_TAVUK_SOTE,        ["tavuk", ING_SOGHAN, "domates"]),
            ("like",  "İskender Kebap",    ["et", "domates salçası", ING_YOGURT]),
            ("like",  "Ali Nazik Kebap",   ["et", ING_PATLICAN, ING_YOGURT]),
            ("like",  "Tavuk Döner",       ["tavuk", ING_SOGHAN, "baharatlar"]),
            ("cook",  RCP_TAVUK_SOTE,        ["tavuk", ING_SOGHAN, "domates"]),
            ("skip",  RCP_SUTLAC,            ["süt", ING_PIRINC, ING_SEKER]),
            ("skip",  "Baklava",           ["un", ING_TEREYAGI, ING_SEKER]),
        ],
        "consumption": [
            (RCP_TAVUK_SIS,     "lunch",  1.0, 5),
            (RCP_TAVUK_SOTE,    "dinner", 1.0, 4),
            ("İskender Kebap", "lunch", 1.0, 5),
        ],
    },
    {
        "id": "seed-user-003-zeynep-demir-000",
        "email": "zeynep.demir@test-buzdolabi.com",
        "display_name": "Zeynep Demir",
        "dietary": {"vegan": True},
        "fridge": ["mercimek", "nohut", "ıspanak", ING_HAVUC, ING_ZEYTINYAGI, "limon", "maydanoz"],
        "interactions": [
            ("like",  RCP_VEGAN_MERCIMEK,          ["mercimek", ING_SOGHAN, "maydanoz"]),
            ("like",  "Vegan Yaprak Sarma (Vegan)",              [ING_ZEYTINYAGI, ING_PIRINC, "limon"]),
            ("like",  "Vegan Mantar Döner (Vegan)",              ["mantar", ING_SOGHAN, "baharatlar"]),
            ("like",  RCP_VEGAN_BIBER_DOLMASI,             ["biber", ING_PIRINC, ING_SOGHAN]),
            ("like",  RCP_MERCIMEK_CORBASI,                         ["mercimek", ING_SOGHAN, ING_HAVUC]),
            ("cook",  RCP_VEGAN_MERCIMEK,          ["mercimek", ING_SOGHAN, "maydanoz"]),
            ("view",  RCP_EZOGELIN_CORBASI,                         ["mercimek", "bulgur"]),
            ("skip",  RCP_KURU_FASULYE,                             ["fasulye", "et", ING_SOGHAN]),
            ("skip",  RCP_ADANA_KEBAP,                              [ING_KIYMA, ING_SOGHAN, "biber"]),
        ],
        "consumption": [
            (RCP_VEGAN_MERCIMEK, "lunch",  1.0, 5),
            (RCP_MERCIMEK_CORBASI,               "dinner", 1.0, 4),
            ("Vegan Yaprak Sarma (Vegan)",     "dinner", 1.5, 5),
        ],
    },
    {
        "id": "seed-user-004-canan-sahin-0000",
        "email": "canan.sahin@test-buzdolabi.com",
        "display_name": "Canan Şahin",
        "dietary": {"vegan": True},
        "fridge": ["mercimek", "bulgur", ING_SOGHAN, "domates", ING_ZEYTINYAGI, "maydanoz", "limon"],
        "interactions": [
            ("like",  RCP_VEGAN_MERCIMEK, ["mercimek", ING_SOGHAN, "maydanoz"]),
            ("like",  RCP_VEGAN_BIBER_DOLMASI,    ["biber", ING_PIRINC, ING_SOGHAN]),
            ("like",  RCP_MERCIMEK_CORBASI,                ["mercimek", ING_SOGHAN, ING_HAVUC]),
            ("like",  RCP_EZOGELIN_CORBASI,                ["mercimek", "bulgur", ING_SOGHAN]),
            ("like",  RCP_ZEYTINYAGLI_YAPRAK_SARMA,        [ING_ZEYTINYAGI, ING_PIRINC, "limon"]),
            ("cook",  RCP_EZOGELIN_CORBASI,                ["mercimek", "bulgur", ING_SOGHAN]),
            ("skip",  RCP_TAVUK_SIS,                       ["tavuk", "biber"]),
            ("skip",  "Etli Güveç",                      ["et", "domates"]),
        ],
        "consumption": [
            (RCP_EZOGELIN_CORBASI,                "lunch",  1.0, 5),
            (RCP_VEGAN_BIBER_DOLMASI,     "dinner", 1.0, 4),
            (RCP_ZEYTINYAGLI_YAPRAK_SARMA,        "lunch",  1.0, 5),
        ],
    },
    {
        "id": "seed-user-005-emre-arslan-0000",
        "email": "emre.arslan@test-buzdolabi.com",
        "display_name": "Emre Arslan",
        "dietary": {},
        "fridge": [ING_KURU_FASULYE, ING_PIRINC, ING_SALCA, ING_SOGHAN, "domates", "et", ING_SARIMSAK],
        "interactions": [
            ("like",  RCP_KURU_FASULYE,              [ING_KURU_FASULYE, ING_SOGHAN, ING_SALCA]),
            ("like",  "Pilav Üstü Kuru Fasulye",   [ING_KURU_FASULYE, ING_PIRINC, ING_SOGHAN]),
            ("like",  RCP_MERCIMEK_CORBASI,           ["mercimek", ING_SOGHAN, ING_HAVUC]),
            ("like",  RCP_ETLI_NOHUT,          ["nohut", "et", ING_SOGHAN]),
            ("like",  "Bulgur Pilavı",              ["bulgur", ING_SOGHAN, ING_SALCA]),
            ("like",  "Tereyağlı Pirinç Pilavı",    [ING_PIRINC, ING_TEREYAGI, "tuz"]),
            ("cook",  RCP_KURU_FASULYE,              [ING_KURU_FASULYE, ING_SOGHAN, ING_SALCA]),
            ("cook",  RCP_ETLI_NOHUT,          ["nohut", "et", ING_SOGHAN]),
            ("view",  RCP_NOHUTLU_PIRINC,      ["nohut", ING_PIRINC]),
        ],
        "consumption": [
            (RCP_KURU_FASULYE,            "lunch",  1.0, 5),
            (RCP_ETLI_NOHUT,       "dinner", 1.0, 5),
            ("Tereyağlı Pirinç Pilavı", "dinner", 1.0, 4),
        ],
    },
    {
        "id": "seed-user-006-fatma-celik-0000",
        "email": "fatma.celik@test-buzdolabi.com",
        "display_name": "Fatma Çelik",
        "dietary": {},
        "fridge": [ING_KURU_FASULYE, "nohut", ING_PIRINC, "domates", ING_SOGHAN, ING_SALCA, "et"],
        "interactions": [
            ("like",  RCP_KURU_FASULYE,             [ING_KURU_FASULYE, ING_SOGHAN, ING_SALCA]),
            ("like",  RCP_ETLI_NOHUT,         ["nohut", "et", ING_SOGHAN]),
            ("like",  RCP_EZOGELIN_CORBASI,           ["mercimek", "bulgur", ING_SOGHAN]),
            ("like",  RCP_ZEYTINYAGLI_YAPRAK_SARMA,   [ING_ZEYTINYAGI, ING_PIRINC, "limon"]),
            ("like",  RCP_NOHUTLU_PIRINC,      ["nohut", ING_PIRINC, ING_SOGHAN]),
            ("like",  "Tavuklu Pilav",              ["tavuk", ING_PIRINC, "baharatlar"]),
            ("cook",  RCP_ETLI_NOHUT,          ["nohut", "et", ING_SOGHAN]),
            ("cook",  RCP_KURU_FASULYE,               [ING_KURU_FASULYE, ING_SOGHAN, ING_SALCA]),
            ("skip",  "Baklava",                    ["un", ING_SEKER, ING_TEREYAGI]),
        ],
        "consumption": [
            (RCP_ETLI_NOHUT,      "dinner", 1.0, 5),
            (RCP_KURU_FASULYE,           "lunch",  1.0, 5),
            (RCP_NOHUTLU_PIRINC,  "dinner", 1.5, 4),
        ],
    },
    {
        "id": "seed-user-007-burak-ozdemir-00",
        "email": "burak.ozdemir@test-buzdolabi.com",
        "display_name": "Burak Özdemir",
        "dietary": {},
        "fridge": [ING_BALIK_FILETO, "limon", ING_ZEYTINYAGI, "maydanoz", ING_SARIMSAK, "tuz", "karabiber"],
        "interactions": [
            ("like",  RCP_BALIK_BUGULAMA,   [ING_BALIK_FILETO, "limon", ING_ZEYTINYAGI]),
            ("like",  "Balık Köfte",      ["balık", ING_SOGHAN, "maydanoz"]),
            ("like",  RCP_MIDYE_DOLMA,      ["midye", ING_PIRINC, "baharatlar"]),
            ("like",  "Patlıcan Salatası",[ING_PATLICAN, ING_ZEYTINYAGI, "limon"]),
            ("like",  "Çoban Salatası",   ["domates", "salatalık", ING_SOGHAN]),
            ("cook",  RCP_BALIK_BUGULAMA,   [ING_BALIK_FILETO, "limon", ING_ZEYTINYAGI]),
            ("view",  RCP_MIDYE_DOLMA,      ["midye", ING_PIRINC]),
            ("skip",  "Baklava",          ["un", ING_SEKER, ING_TEREYAGI]),
        ],
        "consumption": [
            (RCP_BALIK_BUGULAMA,  "dinner", 1.0, 5),
            (RCP_MIDYE_DOLMA,     "lunch",  1.0, 4),
            ("Çoban Salatası",  "lunch",  1.0, 4),
        ],
    },
    {
        "id": "seed-user-008-selin-aydin-0000",
        "email": "selin.aydin@test-buzdolabi.com",
        "display_name": "Selin Aydın",
        "dietary": {},
        "fridge": ["un", "yumurta", ING_TEREYAGI, "süt", ING_SEKER, "tuz", "peynir"],
        "interactions": [
            ("like",  "Baklava",            ["un", ING_TEREYAGI, ING_SEKER]),
            ("like",  RCP_SUTLAC,             ["süt", ING_PIRINC, ING_SEKER]),
            ("like",  "Fırında Sütlaç",     ["süt", ING_PIRINC, ING_SEKER]),
            ("like",  "Peynirli Gözleme",   ["un", "peynir", ING_TEREYAGI]),
            ("like",  "Peynirli Poğaça",    ["un", "peynir", "yumurta"]),
            ("like",  "Ispanaklı Börek",    ["un", "ıspanak", "peynir"]),
            ("cook",  "Baklava",            ["un", ING_TEREYAGI, ING_SEKER]),
            ("cook",  RCP_SUTLAC,             ["süt", ING_PIRINC, ING_SEKER]),
            ("skip",  RCP_ADANA_KEBAP,        [ING_KIYMA, ING_SOGHAN]),
        ],
        "consumption": [
            ("Baklava",           "snack",  1.0, 5),
            (RCP_SUTLAC,            "snack",  1.5, 5),
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
