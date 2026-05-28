from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}
