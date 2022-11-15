from typing import Optional

from backend.apis.version1.route_login import get_current_user_from_token
from backend.db.models.users import User
from backend.db.repository.adventures import create_new_adventure
from backend.db.repository.adventures import list_adventures
from backend.db.repository.adventures import retreive_adventure
from backend.db.repository.adventures import search_adventure
from backend.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from backend.schemas.adventures import AdventureCreate
from sqlalchemy.orm import Session
from backend.webapps.adventures.forms import adventureCreateForm


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    adventures = list_adventures(db=db)
    return templates.TemplateResponse(
        "mada_tretreka/index.html", {"request": request, "adventures": adventures, "msg": msg}
    )

@router.get("/about_us")
async def about_us(request: Request):
    return templates.TemplateResponse(
        "mada_tretreka/about-us.html", {"request": request}
    )

@router.get("/circuit")
async def circuit(request: Request, db: Session = Depends(get_db), msg: str = None):
    circuits = list_adventures(db=db)
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

@router.get("/details/{id}")
def adventure_detail(id: int, request: Request, db: Session = Depends(get_db)):
    adventure = retreive_adventure(id=id, db=db)
    return templates.TemplateResponse(
        "adventures/detail.html", {"request": request, "adventure": adventure}
    )


@router.get("/post-a-adventure/")
def create_adventure(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("adventures/create_adventure.html", {"request": request})


@router.post("/post-a-adventure/")
async def create_adventure(request: Request, db: Session = Depends(get_db)):
    form = adventureCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            adventure = AdventureCreate(**form.__dict__)
            adventure = create_new_adventure(adventure=adventure, db=db)
            return responses.RedirectResponse(
                f"/details/{adventure.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print('error', e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("adventures/create_adventure.html", form.__dict__)
    return templates.TemplateResponse("adventures/create_adventure.html", form.__dict__)


@router.get("/delete-adventure/")
def show_adventures_to_delete(request: Request, db: Session = Depends(get_db)):
    adventures = list_adventures(db=db)
    return templates.TemplateResponse(
        "adventures/show_adventures_to_delete.html", {"request": request, "adventures": adventures}
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    adventures = search_adventure(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "adventures": adventures}
    )
