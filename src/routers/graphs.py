from fastapi import APIRouter

router = APIRouter()


@router.get("/graph/tmp")
async def get_trade_file():
    return {"This has not been implemented yet"}
