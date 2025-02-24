from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .routers import data, files, graphs

app = FastAPI()

origins = ["http://localhost:3000", "http://192.168.50.24:5751"]

app.include_router(data.router)
app.include_router(files.router)
app.include_router(graphs.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
