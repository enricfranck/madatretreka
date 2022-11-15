from fastapi import APIRouter
from backend.webapps.auth import route_login
from backend.webapps.adventures import route_adventures
from backend.webapps.cars import route_cars
from backend.webapps.users import route_users


api_router = APIRouter()
api_router.include_router(route_adventures.router, prefix="", tags=["adventure-webapp"])
api_router.include_router(route_cars.router, prefix="", tags=["cars-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
