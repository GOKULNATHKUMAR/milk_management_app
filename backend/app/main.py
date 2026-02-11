from fastapi import FastAPI
from app.routers import auth, milk_intake, milk_sales, daily_summary
from app.database import Base, engine
from app.routers import reports

app = FastAPI(title="Milk Business App")

app.include_router(auth.router)
app.include_router(milk_intake.router)
app.include_router(milk_sales.router)
app.include_router(daily_summary.router)
app.include_router(reports.router)

# Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
