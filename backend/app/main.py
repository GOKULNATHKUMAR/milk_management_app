from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

app = FastAPI(title="Milk Business App")

app.include_router(auth.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
