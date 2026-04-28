#from fastapi import FastAPI

#app = FastAPI()

#@app.get("/")
#def root():
#    return {"message": "Hello, World!"}

#@app.get("/name/{name}")
#def greet_name(name: str):
#    return {"message:"f"Hello, {name}!"}


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/verdoppeln/{x}")
def verdoppeln(x: int):
    return {"ergebnis": x * 2}
