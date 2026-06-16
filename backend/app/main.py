from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.middleware.rate_limiter import limiter
from datetime import datetime
import time
import logging
from app.config import settings
from app.routes import recipes, auth, feedback, fridge, user_preferences, shopping_list
from app.services.database_service import database_service
from app.services.faiss_service import faiss_service
from app.services.embedding_service import embedding_service
from app.services.reranker_service import reranker_service
from app.services.llm_service import llm_service
from app.services.tfidf_service import tfidf_service

# Setup logger
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Smart Fridge Chef API",
    description="Backend API for Smart Fridge Chef - AI-powered recipe recommendation system",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Response time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))  # ms
    return response

# CORS middleware — includes Capacitor/Ionic origins for iOS build
_cors_origins = [
        "https://akillimutfak.me",
        "https://www.akillimutfak.me",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "capacitor://localhost",   # Capacitor iOS
    "ionic://localhost",        # Ionic iOS
    "http://localhost",         # Capacitor Android / local dev
]
if settings.CORS_EXTRA_ORIGINS:
    _cors_origins += [o.strip() for o in settings.CORS_EXTRA_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)


async def _init_database() -> None:
    try:
        await database_service.init_db()
        logger.info("✅ PostgreSQL (Supabase) database initialized")
    except Exception as e:
        logger.exception(f"❌ Database initialization failed: {e}")


def _init_faiss() -> None:
    try:
        logger.info("📦 Loading FAISS index (Retriever)...")
        success = faiss_service.load_index()
        if success:
            index_info = faiss_service.get_index_info()
            logger.info("✅ FAISS index loaded successfully")
            logger.info(f"   Index type: {index_info.get('index_type', 'unknown')}")
            logger.info(f"   Vectors: {index_info.get('num_vectors', 'unknown')}")
            logger.info(f"   Dimension: {index_info.get('dimension', 'unknown')}")
        else:
            logger.warning("⚠️  FAISS index not found or could not be loaded")
            logger.warning("   Vector search will not be available")
            logger.warning("   Application will continue with string matching fallback")
    except Exception as e:
        logger.exception(f"❌ Error loading FAISS index: {e}")
        logger.warning("   Continuing with string matching fallback")


def _init_tfidf() -> None:
    try:
        logger.info("📋 Loading TF-IDF inverted index...")
        success = tfidf_service.load_index()
        if success:
            logger.info(
                f"✅ TF-IDF index loaded "
                f"({tfidf_service._matrix.shape[0]} tarif, vocab={tfidf_service.vocab_size})"
            )
        else:
            logger.warning("⚠️  TF-IDF index bulunamadı — hibrit retrieval devre dışı")
            logger.warning("   scripts/build_tfidf_index.py ile index oluşturun")
    except Exception as e:
        logger.exception(f"❌ TF-IDF index yüklenemedi: {e}")


def _init_embedding() -> None:
    try:
        logger.info("🔤 Pre-loading embedding model...")
        embedding_service._load_model()
        logger.info(f"✅ Embedding model loaded: {embedding_service.model_name}")
    except Exception as e:
        logger.warning(f"⚠️  Embedding model pre-load failed: {e}")


def _init_reranker() -> None:
    try:
        if reranker_service.enabled:
            logger.info(f"🔄 Pre-loading reranker model: {reranker_service.model_name} ...")
            reranker_service._load_model()
            logger.info("✅ Reranker model loaded")
        else:
            logger.info("⚠️  Reranker is disabled in config")
    except Exception as e:
        logger.warning(f"⚠️  Reranker pre-load failed (will retry on first request): {e}")


def _init_llm() -> None:
    try:
        if llm_service.enabled:
            if llm_service.api_key:
                logger.info(f"🤖 LLM service ready: {llm_service.model_name}")
            else:
                logger.warning("⚠️  GEMINI_API_KEY not found — LLM explanations unavailable")
        else:
            logger.info("⚠️  LLM service is disabled in config")
    except Exception as e:
        logger.warning(f"⚠️  LLM initialization warning: {e}")


def _log_pipeline_summary() -> None:
    logger.info("🔗 RAG Pipeline ready")
    logger.info("   Components:")
    logger.info(f"      - Retriever (FAISS): {'✅' if faiss_service.is_loaded() else '❌ NOT LOADED'}")
    logger.info(f"      - TF-IDF index: {'✅ (hibrit aktif)' if tfidf_service.is_loaded() else '⚠️  yüklü değil (FAISS-only)'}")
    logger.info(f"      - Reranker: {'✅' if reranker_service.is_loaded() else '❌ NOT LOADED'}")
    logger.info(f"      - Generator (LLM): {'✅' if (llm_service.enabled and llm_service.api_key) else '❌'}")
    logger.info("✅ API startup completed - RAG Pipeline ready")


# Startup event - Initialize RAG Pipeline components
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Smart Fridge Chef API...")
    await _init_database()
    _init_faiss()
    _init_tfidf()
    _init_embedding()
    _init_reranker()
    _init_llm()
    _log_pipeline_summary()


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running
    Includes RAG Pipeline component status
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.NODE_ENV,
        "database": {"available": True, "type": "PostgreSQL (Supabase)"},
        "smtp": {
            "enabled": settings.SMTP_ENABLED,
            "configured": bool(settings.SMTP_USER and settings.SMTP_PASSWORD) if settings.SMTP_ENABLED else None
        },
        "rag_pipeline": {
            "retriever": {
                "available": faiss_service.is_loaded(),
                "type": "FAISS"
            },
            "reranker": {
                "available": reranker_service.enabled,
                "loaded": reranker_service.is_loaded() if reranker_service.enabled else False,
                "model": reranker_service.model_name if reranker_service.enabled else None
            },
            "generator": {
                "available": llm_service.is_available(),
                "model": llm_service.model_name if llm_service.enabled else None,
                "has_api_key": bool(llm_service.api_key) if llm_service.enabled else False
            }
        }
    }


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Sunucu hatası. Lütfen daha sonra tekrar deneyin."},
    )


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(fridge.router, prefix="/api")
app.include_router(user_preferences.router, prefix="/api")
app.include_router(shopping_list.router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Smart Fridge Chef API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=True if settings.NODE_ENV == "development" else False
    )
