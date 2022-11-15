from typing import List
from typing import Optional

from backend.apis.version1.route_login import get_current_user_from_token
from backend.db.models.users import User
from backend.db.repository.adventures import create_new_adventure
from backend.db.repository.adventures import delete_adventure_by_id
from backend.db.repository.adventures import list_adventures
from backend.db.repository.adventures import retreive_adventure
from backend.db.repository.adventures import search_adventure
from backend.db.repository.adventures import update_adventure_by_id
from backend.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.templating import Jinja2Templates
from backend.schemas.adventures import AdventureCreate
from backend.schemas.adventures import Showadventure
from sqlalchemy.orm import Session


router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")


@router.post("/create-adventure/", response_model=Showadventure)
def create_adventure(
    adventure: AdventureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    adventure = create_new_adventure(adventure=adventure, db=db, owner_id=current_user.id)
    return adventure


@router.get(
    "/get/{id}", response_model=Showadventure
)  # if we keep just "{id}" . it would stat catching all routes
def read_adventure(id: int, db: Session = Depends(get_db)):
    adventure = retreive_adventure(id=id, db=db)
    if not adventure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"adventure with this id {id} does not exist",
        )
    return adventure


@router.get("/all", response_model=List[Showadventure])
def read_adventures(db: Session = Depends(get_db)):
    adventures = list_adventures(db=db)
    return adventures


@router.put("/update/{id}")
def update_adventure(id: int, adventure: AdventureCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_adventure_by_id(id=id, adventure=adventure, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"adventure with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_adventure(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    adventure = retreive_adventure(id=id, db=db)
    if not adventure:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"adventure with id {id} does not exist",
        )
    delete_adventure_by_id(id=id, db=db, owner_id=current_user.id)
    return {"detail": "Successfully deleted."}
   


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    adventures = search_adventure(term, db=db)
    adventure_titles = []
    for adventure in adventures:
        adventure_titles.append(adventure.title)
    return adventure_titles
