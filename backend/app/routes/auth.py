from fastapi import APIRouter, Response, Depends, HTTPException, Request
import logging
import httpx
from app.middleware.rate_limiter import limiter
from app.models.auth import (
    MagicLinkRequest, MagicLinkVerifyRequest,
    MagicLinkResponse, UserResponse, SessionInfo,
    SupabaseSessionRequest,
)
from app.services.auth_service import auth_service
from app.services.email_service import send_magic_link
from app.middleware.auth import get_current_user
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: Response, session_id: str):
    is_production = settings.NODE_ENV != "development"
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="none" if is_production else "lax",
        secure=is_production,
        max_age=settings.SESSION_EXPIRY_DAYS * 24 * 3600,
    )


@router.post("/supabase-session", response_model=SessionInfo)
@limiter.limit("10/minute")
async def create_supabase_session(request: Request, body: SupabaseSessionRequest, response: Response):
    """
    Validate a Supabase access token, find/create a local user, and issue a session cookie.
    Called by the frontend immediately after supabase.auth.signInWithPassword succeeds.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise HTTPException(
            status_code=503,
            detail="Supabase yapılandırması eksik. SUPABASE_URL ve SUPABASE_ANON_KEY gerekli.",
        )

    # Validate token with Supabase Auth API
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {body.access_token}",
                    "apikey": settings.SUPABASE_ANON_KEY,
                },
            )
    except Exception as exc:
        logger.exception(f"Supabase token validation failed: {exc}")
        raise HTTPException(status_code=503, detail="Supabase bağlantısı kurulamadı.")

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş Supabase token.")

    supabase_user = resp.json()
    email = supabase_user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Token içinde e-posta bulunamadı.")

    # Find or create local user, issue session
    try:
        user = await auth_service.create_or_get_user(email)
        session_id = await auth_service.create_session(user["id"])
        _set_session_cookie(response, session_id)
        session_data = await auth_service.validate_session(session_id)
    except Exception as exc:
        logger.exception(f"DB error in supabase-session for {email}: {exc}")
        raise HTTPException(status_code=500, detail="Veritabanı hatası. Lütfen tekrar deneyin.")

    logger.info(f"Supabase session created for {email}")
    return SessionInfo(
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            display_name=user.get("display_name"),
            created_at=user["created_at"],
        ),
        expires_at=session_data["session_expires_at"],
    )


@router.post("/magic-link", response_model=MagicLinkResponse)
async def request_magic_link(body: MagicLinkRequest):
    user = await auth_service.create_or_get_user(body.email)
    token = await auth_service.generate_magic_link(user["id"])

    logger.info(f"Magic link requested for {body.email}")

    if settings.SMTP_ENABLED:
        if not send_magic_link(body.email, token):
            raise HTTPException(
                status_code=503,
                detail="E-posta gönderilemedi. Lütfen daha sonra tekrar deneyin.",
            )
        dev_token = None
    else:
        dev_token = token if settings.NODE_ENV == "development" else None

    return MagicLinkResponse(
        message="Giriş bağlantısı e-posta adresinize gönderildi",
        dev_token=dev_token,
    )


@router.post("/verify", response_model=SessionInfo)
async def verify_magic_link(body: MagicLinkVerifyRequest, response: Response):
    user = await auth_service.verify_magic_link(body.token)
    if not user:
        raise HTTPException(status_code=400, detail="Geçersiz veya süresi dolmuş bağlantı")

    session_id = await auth_service.create_session(user["id"])
    _set_session_cookie(response, session_id)
    session_data = await auth_service.validate_session(session_id)

    return SessionInfo(
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            display_name=user.get("display_name"),
            created_at=user["created_at"],
        ),
        expires_at=session_data["session_expires_at"],
    )


@router.get("/me", response_model=SessionInfo)
async def get_me(user: dict = Depends(get_current_user)):
    return SessionInfo(
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            display_name=user.get("display_name"),
            created_at=user["created_at"],
        ),
        expires_at=user["session_expires_at"],
    )


@router.post("/logout")
async def logout(response: Response, user: dict = Depends(get_current_user)):
    response.delete_cookie("session_id")
    await auth_service.logout(user.get("session_id", ""))
    logger.info(f"User {user['email']} logged out")
    return {"message": "Çıkış yapıldı"}
