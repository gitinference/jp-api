from src.jp_imports.src.jp_imports.data_process import DataTrade
from src.jp_index.src.data.data_process import DataIndex
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from env import db_credentials
from fastapi import FastAPI
import pandas as pd
import numpy as np
import asyncio
import os

# Initialize DataTrade and DataIndex with db_credentials
dt = DataTrade(db_credentials(), debug=True)
di = DataIndex(db_credentials())

async def init_data(db_url):
    dt = DataTrade(db_url, debug=True)
    di = DataIndex(db_url, debug=True)

    tables = dt.conn.list_tables()
    tasks = []

    # Initialize jptradedata
    if "jptradedata" not in tables or await asyncio.to_thread(dt.conn.table("jptradedata").count().execute) == 0:
        tasks.append(asyncio.to_thread(dt.insert_int_jp, dt.jp_data, dt.agr_file))

    # Wait for jptradedata to be inserted before checking inttradedata
    await asyncio.gather(*tasks)

    # Check and initialize inttradedata
    if "inttradedata" not in tables or await asyncio.to_thread(dt.conn.table("inttradedata").count().execute) == 0:
        tasks.clear()  # Clear the tasks list for new operations
        inttradedata_task = asyncio.to_thread(dt.pull_int_org)
        insert_task = asyncio.to_thread(dt.insert_int_org, dt.org_data)

        # Wait for inttradedata tasks to complete before moving on
        await asyncio.gather(inttradedata_task, insert_task)

    # Initialize consumertable
    if "consumertable" not in tables or await asyncio.to_thread(dt.conn.table("consumertable").count().execute) == 0:
        tasks.append(asyncio.to_thread(di.process_consumer, True))

    # Initialize indicatorstable
    if "indicatorstable" not in tables or await asyncio.to_thread(dt.conn.table("indicatorstable").count().execute) == 0:
        tasks.append(asyncio.to_thread(di.process_jp_index, True))

    # Gather and execute all remaining tasks
    await asyncio.gather(*tasks)
    print("Data initialized successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data(db_credentials())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"message": "Hello World"}

# Endpoint to get the DataFrames
@app.get("/data/trade/jp/")
async def get_data(time:str, types:str, agr:bool=False, group:bool=False,data_filter:str="", agg:str="", update:bool=False):
    df = dt.process_int_org(time=time, types=types, agr=agr, group=group, filter=data_filter, agg=agg, update=update)
    return df.to_pandas().to_dict()

@app.get("/data/trade/org/")
async def get_org_data(time:str, types:str, agr:bool=False, group:bool=False):
    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", f"org_{time}_{types}.parquet")):
        df = dt.process_int_org(time, types, agr, group)
        df.to_parquet(os.path.join(os.getcwd(), "data", "processed", f"org_{time}_{types}.parquet"))
        return df.to_pandas().to_dict()
    else:
        return pd.read_parquet(os.path.join(os.getcwd(), "data", "processed", f"org_{time}_{types}.parquet")).to_dict()

@app.get("/data/trade/moving/")
async def get_moving_data(agr:bool=False):
    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", "moving.parquet")):
        df = dt.process_price(agr=agr)
        df.to_parquet(os.path.join(os.getcwd(), "data", "processed", "moving.parquet"))
        return df.to_pandas().replace([np.nan, np.inf, -np.inf], [0, 0, 0]).to_dict()
    else:
        return pd.read_parquet(os.path.join(os.getcwd(), "data", "processed", "moving.parquet")).replace([np.nan, np.inf, -np.inf], [0, 0, 0]).to_dict()

@app.get("/data/index/consumer")
async def get_consumer(update:bool=False):
    return di.process_consumer(update).to_pandas().to_dict()

@app.get("/data/index/jp_index")
async def get_jp_index(update:bool=False):
    return di.process_jp_index(update).to_pandas().to_dict()

# Endpoints to download files
@app.get("/files/trade/jp/")
async def get_trade_file(time:str, types:str, agr:bool=False, group:bool=False):
    df = dt.process_int_jp(time, types, agr, group)
    file_path = os.path.join(os.getcwd(), "data", f"{time}_{types}.csv")
    df.to_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename=f"{time}_{types}.csv")

@app.get("/files/trade/org/")
async def get_org_file(time:str, types:str, agr:bool=False, group:bool=False):
    file_path = os.path.join(os.getcwd(), "data", "processed", f"org_{time}_{types}.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", f"org_{time}_{types}.csv")):
        df = dt.process_int_org(time, types, agr, group)
        df.to_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename=f"{time}_{types}.csv")

@app.get("/files/trade/moving")
async def get_moving_file(agr:bool=False):
    file_path = os.path.join(os.getcwd(), "data", "processed", "moving.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", "moving.csv")):
        df = dt.process_price(agr=agr)
        df.to_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename="moving.csv")

@app.get("/files/index/consumer")
async def get_consumer_file(update:bool=False):
    df = di.process_consumer(update)
    file_path = os.path.join(os.getcwd(), "data", "consumer.csv") #TODO: Change to temp file
    df.to_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename="consumer.csv")

@app.get("/files/index/jp_index")
async def get_jp_index_file(update:bool=False):
    df = di.process_jp_index(update)
    file_path = os.path.join(os.getcwd(), "data", "jp_index.csv")
    df.to_csv(file_path)
    return FileResponse(file_path, media_type='text/csv', filename="jp_index.csv")
