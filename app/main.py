from fastapi import FastAPI
from app.routes import transaction, users, auth


app = FastAPI(title="Finance Tracker API")

@app.get("/")

def root():
    return {"message": "Finance Tracker API running"}


app.include_router(transaction.router)
app.include_router(users.router)
app.include_router(auth.router)