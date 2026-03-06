from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def create_dummy_data():
    db = SessionLocal()

    if db.query(models.Item).count() == 0:
        items = [
            models.Item(name="Laptop", description="Laptop untuk programming"),
            models.Item(name="Mouse", description="Mouse wireless"),
            models.Item(name="Keyboard", description="Mechanical keyboard")
        ]

        db.add_all(items)
        db.commit()

    db.close()

create_dummy_data()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/", response_model=list[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item