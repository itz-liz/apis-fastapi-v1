from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return {"Hello": "World"}

@app.get("/clientes")
def get_clientes():
    data = [
        {
            "nombre":"Dejah"
        },
        {
            "nombre":"John"
        }
    ]
    return data