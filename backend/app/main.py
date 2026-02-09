from fastapi import FastAPI
from app.routers import auth, milk_intake
from app.database import Base, engine

app = FastAPI(title="Milk Business App")

app.include_router(auth.router)
app.include_router(milk_intake.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
