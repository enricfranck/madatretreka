from backend.db.models.adventures import Adventure
from backend.schemas.adventures import AdventureCreate
from sqlalchemy.orm import Session


def create_new_adventure(adventure: AdventureCreate, db: Session):
    adventure_object = Adventure(**adventure.dict())
    db.add(adventure_object)
    db.commit()
    db.refresh(adventure_object)
    return adventure_object


def retreive_adventure(id: int, db: Session):
    item = db.query(Adventure).filter(Adventure.id == id).first()
    return item


def list_adventures(db: Session):
    adventures = db.query(Adventure).all()
    return adventures


def update_adventure_by_id(id: int, adventure: AdventureCreate, db: Session, owner_id):
    existing_adventure = db.query(Adventure).filter(Adventure.id == id)
    if not existing_adventure.first():
        return 0
    adventure.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_adventure.update(Adventure.__dict__)
    db.commit()
    return 1


def delete_adventure_by_id(id: int, db: Session, owner_id):
    existing_adventure = db.query(Adventure).filter(Adventure.id == id)
    if not existing_adventure.first():
        return 0
    existing_adventure.delete(synchronize_session=False)
    db.commit()
    return 1


def search_adventure(query: str, db: Session):
    adventures = db.query(Adventure).filter(Adventure.traject.contains(query))
    return adventures
