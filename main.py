from src.jp_imports.src.jp_imports.data_process import DataProcess
from fastapi.responses import FileResponse
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/data/imports/")
async def get_data(time:str, types:str, agr:bool=False, group:bool=False, update:bool=False):
    dp = DataProcess("data/")
    df = dp.process_int_jp(time, types, agr, group, update).collect()
    return df.to_dicts()

@app.get("/files/imports/")
async def get_file(time:str, types:str, agr:bool=False, group:bool=False, update:bool=False):
    dp = DataProcess("data/")
    df = dp.process_int_jp(time, types, agr, group, update).collect()
    file_path = os.path.join(os.getcwd(), "data", f"{time}_{types}.csv")
    df.write_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename=f"{time}_{types}.csv")
