import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from routers import chat, leads, widget
from services.supabase import check_connection

logger = logging.getLogger("leadqualify")

_supabase_connected = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _supabase_connected
    try:
        await check_connection()
        _supabase_connected = True
        logger.info("✓ Supabase connection verified successfully")
    except Exception as e:
        logger.warning(f"⚠ Supabase connection check failed: {e}")
    yield


app = FastAPI(title="LeadQualify API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat")
app.include_router(leads.router, prefix="/leads")
app.include_router(widget.router, prefix="/widget")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "supabase_connected": _supabase_connected,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
