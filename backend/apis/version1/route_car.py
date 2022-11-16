import os
from typing import List
from typing import Optional

from backend.apis.version1.route_login import get_current_user_from_token
from backend.db.models.users import User
from backend.db.repository.cars import create_new_car
from backend.db.repository.cars import delete_car_by_id
from backend.db.repository.cars import list_cars
from backend.db.repository.cars import retreive_car
from backend.db.repository.cars import search_car
from backend.db.repository.cars import update_car_by_id
from backend.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi import HTTPException
from fastapi import status
from fastapi.templating import Jinja2Templates
from backend.schemas.cars import CarCreate
from backend.schemas.cars import ShowCar
from sqlalchemy.orm import Session


router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")


@router.post("/create-car/", response_model=ShowCar)
def create_car(
    car: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    car = create_new_car(car=car, db=db, owner_id=current_user.id)
    return car


@router.get(
    "/get/{id}", response_model=ShowCar
)  # if we keep just "{id}" . it would stat catching all routes
def read_car(id: int, db: Session = Depends(get_db)):
    car = retreive_car(id=id, db=db)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"car with this id {id} does not exist",
        )
    return car


@router.get("/all", response_model=List[ShowCar])
def read_cars(db: Session = Depends(get_db)):
    cars = list_cars(db=db)
    return cars


@router.put("/update/{id}")
def update_car(id: int, car: CarCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_car_by_id(id=id, car=car, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"car with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_car(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    car = retreive_car(id=id, db=db)
    if not car:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"car with id {id} does not exist",
        )
    delete_car_by_id(id=id, db=db, owner_id=current_user.id)
    return {"detail": "Successfully deleted."}
   


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    cars = search_car(term, db=db)
    car_titles = []
    for car in cars:
        car_titles.append(car.title)
    return car_titles

@router.get("/image/")
def get_file(name_file: str):
    path = os.getcwd() + "/backend/files/" + name_file
    print(path)
    if os.path.exists(path):
        print(path)
        return FileResponse(path=path)
    else:
        return "No result"