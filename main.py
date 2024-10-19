from src.jp_imports.src.jp_imports.data_process import DataProcess as DataTrade
from src.jp_index.src.data.data_process import DataProcess as DataIndex
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi import FastAPI
import os

load_dotenv()

app = FastAPI()
dp = DataTrade(str(os.environ.get("DATABASE_URL")))
di = DataIndex(str(os.environ.get("DATABASE_URL")))

@app.get("/")
def index():
    return {"message": "Hello World"}

# Endpoint to get the DataFrames
@app.get("/data/trade/")
async def get_data(time:str, types:str, agr:bool=False, group:bool=False, update:bool=False):
    df = dp.process_int_jp(time, types, agr, group, update)
    return df.to_dicts()

@app.get("/data/index/consumer")
async def get_consumer(update:bool=False):
    return di.consumer_data(update).to_dicts()

@app.get("/data/index/jp_index")
async def get_jp_index(update:bool=False):
    dp = DataIndex(str(os.environ.get("DATABASE_URL")))
    return dp.jp_index_data(update).to_dicts()

# Endpoints to download files
@app.get("/files/trade/")
async def get_trade_file(time:str, types:str, agr:bool=False, group:bool=False, update:bool=False):
    dp = DataTrade()
    df = dp.process_int_jp(time, types, agr, group, update)
    file_path = os.path.join(os.getcwd(), "data", f"{time}_{types}.csv")
    df.write_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename=f"{time}_{types}.csv")

@app.get("/files/index/consumer")
async def get_consumer_file(update:bool=False):
    df = di.consumer_data(update)
    file_path = os.path.join(os.getcwd(), "data", "consumer.csv") #TODO: Change to temp file
    df.write_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename="consumer.csv")

@app.get("/files/index/jp_index")
async def get_jp_index_file(update:bool=False):
    df = di.jp_index_data(update)
    file_path = os.path.join(os.getcwd(), "data", "jp_index.csv")
    df.write_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename="jp_index.csv")
