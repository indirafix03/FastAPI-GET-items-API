from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# =====================
# FAKE AUTH (MINIMAL)
# =====================
fake_users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"},
}

def authenticate(token: str):
    user = fake_users.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


# =====================
# DB DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================
# AUTH
# =====================
@app.post("/login")
def login(data: dict):
    user = fake_users.get(data["username"])
    if user and user["password"] == data["password"]:
        return {"access_token": user["username"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# =====================
# CRUD
# =====================
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    return crud.create_item(db, item.name, item.description)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    updated = crud.update_item(db, item_id, item.name, item.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@app.delete("/items/{item_id}")
def delete_item(item_id: int, token: str, db: Session = Depends(get_db)):
    user = authenticate(token)

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    deleted = crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Deleted"}