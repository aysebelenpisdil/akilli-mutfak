"""
Supabase Admin: Mevcut kullanıcıya şifre ata.

Kullanım:
    python scripts/set_supabase_password.py

Çalıştırmadan önce aşağıdaki ortam değişkenlerini ayarlayın (backend/.env):
    SUPABASE_URL=https://taehbletloawnnnyvogn.supabase.co
    SUPABASE_SERVICE_ROLE_KEY=<Dashboard > Settings > API > service_role (secret)>

Hedef kullanıcı ve şifre bu dosyada sabittir — demo sonrası silin.
"""

import os, sys, urllib.request, json, urllib.error

TARGET_EMAIL = "aysebelenpisdil@gmail.com"
NEW_PASSWORD  = "523103"

# --- Env / config -----------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

SUPABASE_URL      = os.environ.get("SUPABASE_URL", "").rstrip("/")
SERVICE_ROLE_KEY  = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    print("HATA: backend/.env dosyasında SUPABASE_URL ve SUPABASE_SERVICE_ROLE_KEY eksik.")
    print("  SUPABASE_URL=https://taehbletloawnnnyvogn.supabase.co")
    print("  SUPABASE_SERVICE_ROLE_KEY=<Dashboard > Settings > API > service_role key>")
    sys.exit(1)

# --- 1. Kullanıcıyı bul -----------------------------------------------------
print(f"[1/3] Kullanıcı aranıyor: {TARGET_EMAIL}")

list_url = f"{SUPABASE_URL}/auth/v1/admin/users?email={TARGET_EMAIL}"
req = urllib.request.Request(
    list_url,
    headers={"apikey": SERVICE_ROLE_KEY, "Authorization": f"Bearer {SERVICE_ROLE_KEY}"},
)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
except urllib.error.HTTPError as e:
    print(f"HATA (list users): {e.code} {e.read().decode()}")
    sys.exit(1)

users = data.get("users", [])
user = next((u for u in users if u.get("email") == TARGET_EMAIL), None)

if not user:
    print(f"Kullanıcı bulunamadı — yeni hesap oluşturuluyor: {TARGET_EMAIL}")
    # --- 2b. Yeni kullanıcı oluştur -----------------------------------------
    create_url = f"{SUPABASE_URL}/auth/v1/admin/users"
    payload = json.dumps({
        "email": TARGET_EMAIL,
        "password": NEW_PASSWORD,
        "email_confirm": True,
    }).encode()
    req = urllib.request.Request(
        create_url, data=payload, method="POST",
        headers={
            "apikey": SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            created = json.loads(r.read())
        print(f"[2/3] Kullanıcı oluşturuldu: {created.get('id')}")
        user_id = created["id"]
    except urllib.error.HTTPError as e:
        print(f"HATA (create user): {e.code} {e.read().decode()}")
        sys.exit(1)
else:
    user_id = user["id"]
    print(f"[2/3] Kullanıcı bulundu: {user_id}")

# --- 3. Şifreyi güncelle ----------------------------------------------------
print(f"[3/3] Şifre güncelleniyor...")
update_url = f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}"
payload = json.dumps({"password": NEW_PASSWORD, "email_confirm": True}).encode()
req = urllib.request.Request(
    update_url, data=payload, method="PUT",
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    },
)
try:
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    print(f"BAŞARILI: {TARGET_EMAIL} kullanıcısına şifre '{NEW_PASSWORD}' atandı.")
    print(f"  Supabase User ID: {result.get('id')}")
    print(f"  Email confirmed:  {result.get('email_confirmed_at')}")
except urllib.error.HTTPError as e:
    print(f"HATA (update password): {e.code} {e.read().decode()}")
    sys.exit(1)
