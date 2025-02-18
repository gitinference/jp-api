from fastapi import APIRouter
from ..submodules.jp_imports.src.data.data_process import DataTrade
from ..submodules.jp_index.src.data.data_process import DataIndex
import numpy as np
import os

router = APIRouter()
dt = DataTrade(database_file="data/data.ddb")
di = DataIndex(database_file="data/data.ddb")


@router.get("/data/trade/jp/")
async def get_jp_data(
    level: str,
    time_frame: str,
    agriculture_filter: bool,
    group: bool,
    level_filter: str,
):
    df = dt.process_int_jp(
        level=level,
        time_frame=time_frame,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
    )
    return df.to_pandas().to_dict()


@router.get("/data/trade/jp/hts_codes/")
async def get_data():
    df = dt.process_int_jp(level_filter="", level="hts", time_frame="yearly")
    df = df.mutate(
        hts_code_first2=df.hts_code.substr(0, 2)
    )  # Extraer las primeras dos posiciones
    unique_first2_codes_df = df.select(df.hts_code_first2).distinct()  # Valores únicos
    unique_first2_codes = (
        unique_first2_codes_df.execute()["hts_code_first2"]
        .dropna()
        .sort_values()
        .to_list()
    )
    return {"hts_code_first2": unique_first2_codes}


@router.get("/data/trade/org/")
async def get_org_data(
    level: str,
    time_frame: str,
    agriculture_filter: bool,
    group: bool,
    level_filter: str,
):
    df = dt.process_int_org(
        level=level,
        time_frame=time_frame,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
    )
    return df.to_pandas().to_dict()


@router.get("/data/trade/moving/")
async def get_moving_data():
    df = dt.process_price()
    df.to_parquet(os.path.join(os.getcwd(), "data", "processed", "moving.parquet"))
    return df.to_pandas().replace([np.nan, np.inf, -np.inf], [0, 0, 0]).to_dict()


@router.get("/data/index/consumer")
async def get_consumer(update: bool = False):
    return di.process_consumer(update).to_pandas().to_dict()


@router.get("/data/index/jp_index")
async def get_jp_index(update: bool = False):
    return (
        di.process_jp_index(update)
        .to_pandas()
        .replace([np.nan, np.inf, -np.inf], [0, 0, 0])
        .to_dict()
    )
