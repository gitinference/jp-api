from fastapi import APIRouter
#from ..submodules.jp_qcew.src.visualization.graph import graphGenerator

router = APIRouter()


# @router.get("/graph/tmp")
# async def get_trade_file(
#     naics_code : str
# ):
#     graph = graphGenerator().create_graph(naics_code)
#     return graph.to_json()
