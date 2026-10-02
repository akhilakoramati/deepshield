from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .core.config import CORS_ORIGINS
from .core.errors import database_error_handler, unexpected_error_handler, validation_error_handler
from .database import Base, engine
from .models import AnalysisResult, Report, UploadedFile, User  # noqa: F401
from .routers import analysis, auth, dashboard, files, history, media, reports, users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="DeepShield API", version="1.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "deepshield-api", "model": "mock", "database": engine.url.get_backend_name()}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(media.router)
app.include_router(files.router)
app.include_router(analysis.router)
app.include_router(history.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
