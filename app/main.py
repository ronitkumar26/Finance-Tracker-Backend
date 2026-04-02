from fastapi import FastAPI

app = FastAPI(title="Finance Tracker API")

@app.get("/")

def root():
    return {"message": "Finance Tracker API running"}