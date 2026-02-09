from fastapi import FastAPI
from app.routers import auth, milk_intake, milk_sales
from app.database import Base, engine

app = FastAPI(title="Milk Business App")

app.include_router(auth.router)
app.include_router(milk_intake.router)
app.include_router(milk_sales.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
