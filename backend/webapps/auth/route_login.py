from backend.apis.version1.route_login import login_for_access_token
from backend.db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/logout/")
def logout(request: Request):
    response = templates.TemplateResponse("auth/login.html", {"request": request})
    response.delete_cookie(key="access_token")
    return response
