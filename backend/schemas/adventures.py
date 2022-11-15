from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# shared properties
class AdventureBase(BaseModel):
    date: Optional[str] = None
    traject: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()


# this will be used to validate data while creating a adventure
class AdventureCreate(AdventureBase):
    date: str
    traject: str
    description: str


# this will be used to format the response to not to have id,owner_id etc
class Showadventure(AdventureBase):
    date: str
    traject: str
    date_posted: date
    description: Optional[str]

    class Config:  # to convert non dict obj to json
        orm_mode = True
