from backend.apis.base import api_router
from backend.core.config import settings
from backend.db.base import Base
from backend.db.session import engine
from backend.db.utils import check_db_connected
from backend.db.utils import check_db_disconnected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.webapps.base import api_router as web_app_router


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
