from __future__ import annotations

import importlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.admin.site import AdminSite
from src.apps.core.exceptions import generic_exception_handler, http_exception_handler
from src.apps.core.middleware import RequestLogMiddleware
from src.apps.interactions.dependencies import TargetValidator
from src.core.config import settings
from src.core.database import close_db, init_db
from src.core.logger import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger(__name__)

# ── App Registry ──

ENABLED_APPS = [
    "src.apps.users",
    "src.apps.forum",
    "src.apps.interactions",
    "src.apps.experthub",
    "src.apps.jobhub",
]

# Global admin site
admin_site = AdminSite()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    logger.info(
        "Application starting",
        env=settings.APP_ENV,
        apps=ENABLED_APPS,
    )

    # Initialize database (dev mode)
    if settings.is_dev:
        await init_db()

    # Register dependency overrides
    try:
        forum_deps = importlib.import_module("src.apps.forum.dependencies")
        if hasattr(forum_deps, "validate_forum_target"):
            app.dependency_overrides[TargetValidator] = forum_deps.validate_forum_target
            logger.info("Registered TargetValidator override from forum app")
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not register TargetValidator: {e}")

    yield

    # Shutdown
    await close_db()
    logger.info("Application shutdown")


# ── Create App ──

app = FastAPI(
    title="MyWeb API",
    description="FastAPI pluggable app architecture backend",
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# ── Middleware ──

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Environment", "X-API-Version"],
)

app.add_middleware(RequestLogMiddleware)

# ── Exception Handlers ──

app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, generic_exception_handler)  # type: ignore[arg-type]

# ── Pluggable App Loading ──

for app_path in ENABLED_APPS:
    try:
        # Load router
        router_module = importlib.import_module(f"{app_path}.router")
        app.include_router(router_module.router, prefix=settings.API_V1_PREFIX)
        logger.info(f"Loaded router: {app_path}.router")

        # Load admin registration
        admin_module = importlib.import_module(f"{app_path}.admin")
        if hasattr(admin_module, "register_admin"):
            admin_module.register_admin(admin_site)
            logger.info(f"Loaded admin: {app_path}.admin")
    except ModuleNotFoundError as e:
        logger.warning(f"Failed to load app {app_path}: {e}")

# Register admin routes
# app.include_router(admin_site.router)
app.include_router(admin_site.router, prefix=settings.API_V1_PREFIX)
# ── Health Check ──


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "version": settings.API_VERSION, "env": settings.APP_ENV}
