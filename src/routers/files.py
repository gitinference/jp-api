from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..submodules.jp_imports.src.data.data_process import DataTrade
import pandas as pd
import io
from fastapi.responses import StreamingResponse
from .data import get_indicators_dict

# from ..submodules.jp_index.src.data.data_process import DataIndex
import os

router = APIRouter()
dt = DataTrade(database_file="data/data.ddb")
# di = DataIndex(database_file="data/data.ddb")

@router.get("/files/trade/jp/")
async def get_trade_file(
    level: str,
    time_frame: str,
    agriculture_filter: bool = False,
    group: bool = False,
    level_filter: str = "",
):
    df = dt.process_int_jp(
        level=level,
        time_frame=time_frame,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
    )
    file_path = os.path.join(os.getcwd(), "data", f"{time_frame}_{level}.csv")
    df.write_csv(file_path)
    return FileResponse(
        file_path, media_type="text/csv", filename=f"{time_frame}_{level}.csv"
    )


@router.get("/files/trade/org/")
async def get_org_file(
    level: str,
    time_frame: str,
    agriculture_filter: bool,
    group: bool,
    level_filter: str,
):
    file_path = os.path.join(
        os.getcwd(), "data", "processed", f"org_{time_frame}_{level}.csv"
    )

    df = dt.process_int_org(
        level=level,
        time_frame=time_frame,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
    )
    df.write_csv(file_path)
    return FileResponse(
        file_path, media_type="text/csv", filename=f"{time_frame}_{level_filter}.csv"
    )

@router.get("/files/trade/indicators/")
async def get_indicators_file(time_frame: str):
    data = get_indicators_dict(time_frame)
    if isinstance(data, dict) and "error" in data:
        return data  # Retorna el error como JSON
    
    # Convierte la lista de dicts en DataFrame
    df = pd.DataFrame(data)
    # Exporta el DataFrame a CSV en memoria
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
    # Retorna el archivo CSV para descarga
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={time_frame}.csv"}
    )
    
    
@router.get("/files/trade/moving")
async def get_moving_file():
    file_path = os.path.join(os.getcwd(), "data", "processed", "moving.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", "moving.csv")):
        df = dt.process_price()
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename="moving.csv")


# @router.get("/files/index/consumer")
# async def get_consumer_file(update: bool = False):
#     df = di.process_consumer(update)
#     file_path = os.path.join(
#         os.getcwd(), "data", "consumer.csv"
#     df.to_csv(file_path)
#     return FileResponse(file_path, media_type="text/csv", filename="consumer.csv")
#
#
# @router.get("/files/index/jp_index")
# async def get_jp_index_file(update: bool = False):
#     df = di.process_jp_index(update)
#     file_path = os.path.join(os.getcwd(), "data", "jp_index.csv")
#     df.write_csv(file_path)
#     return FileResponse(file_path, media_type="text/csv", filename="jp_index.csv")
