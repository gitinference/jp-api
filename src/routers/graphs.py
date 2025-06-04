from fastapi import APIRouter
# from ..submodules.jp_qcew.src.visualization.graph import graphGenerator
from ..submodules.jp_imports.src.graphs.graphs import DataGraph

router = APIRouter()


# @router.get("/graph/tmp")
# async def get_trade_file(
#     naics_code : str
# ):
#     graph = graphGenerator().create_graph(naics_code)
#     return graph.to_json()

@router.get("/graph/import-export/")
async def get_imports_exports_graph(
    level: str,
    time_frame: str,
    agriculture_filter: bool = False,
    group: bool = False,
    level_filter: str = "",
    datetime: str = "",
    frequency: str = "",
    second_dropdown: str = "",
    third_dropdown: str = "",
    type: str = "",
):
    if type == "imports":
        graph = DataGraph().gen_imports_chart(
            level = level,
            time_frame = time_frame,
            agriculture_filter = agriculture_filter,
            group = group,
            level_filter = level_filter,
            datetime = datetime,
            frequency=frequency,
            second_dropdown = second_dropdown,
            third_dropdown = third_dropdown,
        )
    elif type == "exports":
        graph = DataGraph().gen_exports_chart(
            level = level,
            time_frame = time_frame,
            agriculture_filter = agriculture_filter,
            group = group,
            level_filter = level_filter,
            datetime = datetime,
            frequency=frequency,
            second_dropdown = second_dropdown,
            third_dropdown = third_dropdown,
        )
    else:
        raise ValueError("Invalid type specified. Use 'imports' or 'exports'.")
    return graph.to_html()

@router.get("/graph/product-hts/")
async def get_product_hts_graph(
    level: str,
    agriculture_filter: bool = False,
    group: bool = False,
    level_filter: str = "",
    time_frame: str = "",
    trade_type: str = "",
):
    graph, context = DataGraph().gen_hts_chart(
        level=level,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
        frequency=time_frame,
        trade_type=trade_type
    )
    return graph.to_html(), context

@router.get("/graph/product-ranking/")
async def get_hts_ranking_graph():
    graphs = DataGraph().gen_hts_ranking_chart()
    return {
            "export_top": graphs['export_top'].to_html(),
            "export_bottom": graphs['export_bottom'].to_html(),
            "import_top": graphs['import_top'].to_html(),
            "import_bottom": graphs['import_bottom'].to_html()
        }