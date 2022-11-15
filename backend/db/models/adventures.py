from backend.db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Adventure(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    traject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_posted = Column(Date)
