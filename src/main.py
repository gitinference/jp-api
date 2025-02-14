from fastapi import FastAPI

from .routers import data, files, graphs

app = FastAPI()

app.include_router(data.router)
app.include_router(files.router)
app.include_router(graphs.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
