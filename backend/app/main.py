from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import cases, health, legal_terms
from app.core.config import get_settings
from app.db.bootstrap import bootstrap_database
from app.db.session import SessionLocal, engine
from app.providers.db_case_provider import DbCaseProvider


def create_app() -> FastAPI:
    settings = get_settings()
    bootstrap_database(engine, Path("data/sample_cases.json"))
    app = FastAPI(title="Easy Case Law Backend", version="0.1.0")
    app.state.case_provider = DbCaseProvider(session_factory=SessionLocal)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(cases.router, prefix="/api", tags=["cases"])
    app.include_router(legal_terms.router, prefix="/api", tags=["legal-terms"])
    return app


app = create_app()
