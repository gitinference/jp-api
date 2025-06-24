import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from ..submodules.jp_imports.src.data.data_process import DataTrade
from ..submodules.jp_index.src.data.data_process import DataIndex
from ..submodules.jp_qcew.src.data.data_process import cleanData

router = APIRouter()
dt = DataTrade(database_file="data/data.ddb")
di = DataIndex(database_file="data/data.ddb")
dc = cleanData(database_file="data/data.ddb")


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


@router.get("/files/index/indicators/")
async def get_indicators_file(
    time_frame: str,
):
    try:
        file_path = os.path.join(
            os.getcwd(), "data", "processed", f"jp_indicators_{time_frame}.csv"
        )
        df = di.jp_indicator_data(time_frame=time_frame)
        df.write_csv(file_path)
        return FileResponse(
            file_path, media_type="text/csv", filename=f"jp_indicators_{time_frame}.csv"
        )
    except ValueError:
        return {"error": "invalid timeframe"}
    
@router.get("/files/qcew/employment/")
async def get_qcew_employment_file(
    time_frame: str,
):
    try:
        file_path = os.path.join(
            os.getcwd(), "data", "processed", f"qcew_employment_{time_frame}.csv"
        )
        df, naics = dc.get_naics_data(naics_code=time_frame)
        df.write_csv(file_path)
        return FileResponse(
            file_path, media_type="text/csv", filename=f"qcew_employment_{time_frame}.csv"
        )
    except ValueError:
        return {"error": "invalid timeframe"}
    
@router.get("/files/index/consumer_index/")
async def get_consumer_file(
    time_frame: str,
    level: str
):
    try:
        file_path = os.path.join(
            os.getcwd(), "data", "processed", f"{level}_consumer_index_{time_frame}.csv"
        )
        df = di.process_consumer_data(time_frame=time_frame, data_type=level)
        df.write_csv(file_path)
        return FileResponse(
            file_path, media_type="text/csv", filename=f"{level}_consumer_index_{time_frame}.csv"
        )
    except ValueError:
        return {"error": "invalid timeframe"}


@router.get("/files/trade/moving")
async def get_moving_file():
    file_path = os.path.join(os.getcwd(), "data", "processed", "moving.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", "moving.csv")):
        df = dt.process_price()
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename="moving.csv")

@router.get("/files/index/awards/secter")
async def get_awards_secter_file(
    time_frame: str,
    level: str
):
    file_path = os.path.join(os.getcwd(), "data", "processed", "awards_secter.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", f"{time_frame}_awards_secter.csv")):
        df, columns = di.process_awards_by_secter(time_frame, level)
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename=f"{time_frame}_awards_secter.csv")

@router.get("/files/index/awards/category")
async def get_awards_category_file(
    dropdown: int = 2013,
    second_dropdown: int = 1,
    third_dropdown: str = 'awarding_agency_name',
    time_frame: str = 'yearly',
):
    file_path = os.path.join(os.getcwd(), "data", "processed", "awards_category.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", f"{time_frame}_awards_category.csv")):
        df, columns = di.process_awards_by_category(dropdown, second_dropdown, second_dropdown, time_frame, third_dropdown)
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename=f"{time_frame}_awards_category.csv")

@router.get("/files/index/energy/")
async def get_energy_file(
    time_frame: str = "monthly",
    level: str = "",
):
    file_path = os.path.join(os.getcwd(), "data", "processed", "energy.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", "energy.csv")):
        df, columns  = di.process_energy_data(time_frame, level)
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename="energy.csv")

@router.get("/files/index/demographic/")
async def get_demographic_file(
    time_frame: str,
):
    file_path = os.path.join(os.getcwd(), "data", "processed", f"{time_frame}_demographic.csv")

    if not os.path.exists(os.path.join(os.getcwd(), "data", "processed", f"{time_frame}_demographic.csv")):
        df = di.jp_demographic_data(time_frame)
        df.write_csv(file_path)
    return FileResponse(file_path, media_type="text/csv", filename=f"{time_frame}_demographic.csv")

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
