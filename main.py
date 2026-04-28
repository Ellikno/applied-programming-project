
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/verdoppeln/{x}")
def verdoppeln(x: int):
    return {"ergebnis": x * 2}
