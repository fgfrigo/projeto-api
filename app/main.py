from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from dotenv import load_dotenv

load_dotenv()

from app.db import get_db, init_db, Item
from app.core.auth import require_auth
from app.routes.external import router as external_router

app = FastAPI(title="External API (SQLite)")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(external_router)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/items")
def list_items(
    _auth=Depends(require_auth),
    db: Session = Depends(get_db),
):
    items = db.execute(select(Item)).scalars().all()
    return [{"id": i.id, "name": i.name} for i in items]

@app.post("/items")
def create_item(
    payload: dict,
    _auth=Depends(require_auth),
    db: Session = Depends(get_db),
):
    name = (payload or {}).get("name")
    if not name:
        raise HTTPException(400, "Missing 'name'")
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}

@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    payload: dict,
    _auth=Depends(require_auth),
    db: Session = Depends(get_db),
):
    name = (payload or {}).get("name")
    if not name:
        raise HTTPException(400, "Missing 'name'")
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    item.name = name
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    _auth=Depends(require_auth),
    db: Session = Depends(get_db),
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
