from backend.apis.version1 import route_adventure
from backend.apis.version1 import route_login
from backend.apis.version1 import route_users
from backend.apis.version1 import route_car
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_adventure.router, prefix="/adventures", tags=["adventures"])
api_router.include_router(route_car.router, prefix="/cars", tags=["cars"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
