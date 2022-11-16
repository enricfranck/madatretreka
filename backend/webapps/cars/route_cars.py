import os
from typing import Optional

from backend.apis.version1.route_login import get_current_user_from_token
from backend.db.models.users import User
from backend.db.repository.cars import create_new_car
from backend.db.repository.cars import list_cars
from backend.db.repository.cars import retreive_car
from backend.db.repository.cars import search_car
from backend.db.session import get_db
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from backend.schemas.cars import CarCreate
from sqlalchemy.orm import Session
from backend.webapps.cars.forms import carCreateForm


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)


@router.get("/cars")
async def cars(request: Request, db: Session = Depends(get_db), msg: str = None):
    cars = list_cars(db=db)
    return templates.TemplateResponse(
        "mada_tretreka/car.html", {"request": request, "cars": cars, "msg": msg}
    )

@router.get("/about_us")
async def about_us(request: Request):
    return templates.TemplateResponse(
        "mada_tretreka/about-us.html", {"request": request}
    )

@router.get("/circuit")
async def circuit(request: Request, db: Session = Depends(get_db), msg: str = None):
    circuits = list_cars(db=db)
    return templates.TemplateResponse(
        "mada_tretreka/circuit.html", {"request": request, "circuits": circuits, "msg": msg}
    )

@router.get("/customer_protection")
async def customer_protection(request: Request):
    return templates.TemplateResponse(
        "mada_tretreka/customer-protection.html", {"request": request}
    )

@router.get("/our_offer")
async def our_offer(request: Request):
    return templates.TemplateResponse(
        "mada_tretreka/our-offer.html", {"request": request}
    )

@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse(
        "mada_tretreka/contact.html", {"request": request}
    )

@router.get("/details-car/{id}")
def car_detail(id: int, request: Request, db: Session = Depends(get_db)):
    car = retreive_car(id=id, db=db)
    return templates.TemplateResponse(
        "cars/detail.html", {"request": request, "car": car}
    )


@router.get("/post-a-cars/")
def create_car(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("cars/create_car.html", {"request": request})


@router.post("/post-a-cars/")
async def create_car(request: Request, db: Session = Depends(get_db)):
    form = carCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            car = CarCreate(**form.__dict__)
            car = create_new_car(car=car, db=db)
            return responses.RedirectResponse(
                f"/details-car/{car.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print('error', e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("cars/create_car.html", form.__dict__)
    return templates.TemplateResponse("cars/create_car.html", form.__dict__)


@router.get("/delete-cars/")
def show_cars_to_delete(request: Request, db: Session = Depends(get_db)):
    cars = list_cars(db=db)
    return templates.TemplateResponse(
        "cars/show_cars_to_delete.html", {"request": request, "cars": cars}
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    cars = search_car(query, db=db)
    return templates.TemplateResponse(
        "cars/show_cars_to_delete.html", {"request": request, "cars": cars}
    )



@router.get("/image/")
def get_file(name_file: str):
    path = os.getcwd() + "/backend/files/" + name_file
    print(path)
    if os.path.exists(path):
        print(path)
        return FileResponse(path=path)
    else:
        return "No result"

@router.post("/upload/")
async def create_upload_file(*,
                             uploaded_file: UploadFile = File(...), name_image: str
                             ):
    name_image = name_image.replace(" ", "_")
    name = list(os.path.splitext(uploaded_file.filename))[1]
    allowed_files = {".jpg", ".jpeg", ".png"}

    if name.lower() not in allowed_files:
        raise HTTPException(status_code=402, detail="invalid image")
    file_location = f"backend/files/{name_image}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"filename": f'{name_image}'}
