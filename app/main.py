from fastapi import FastAPI
from app.routes import transaction


app = FastAPI(title="Finance Tracker API")

@app.get("/")

def root():
    return {"message": "Finance Tracker API running"}


app.include_router(transaction.router)