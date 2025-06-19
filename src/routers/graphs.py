from fastapi import APIRouter
from ..submodules.jp_qcew.src.visualization.graph import graphGenerator
from ..submodules.jp_imports.src.graphs.graphs import DataGraph
from ..submodules.jp_index.src.graphs import DataGraph as IndexDataGraph

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
        graph, hts_codes = DataGraph(database_file="data/data.ddb").gen_imports_chart(
            level=level,
            time_frame=time_frame,
            agriculture_filter=agriculture_filter,
            group=group,
            level_filter=level_filter,
            datetime=datetime,
            frequency=frequency,
            second_dropdown=second_dropdown,
            third_dropdown=third_dropdown,
        )
    elif type == "exports":
        graph, hts_codes = DataGraph(database_file="data/data.ddb").gen_exports_chart(
            level=level,
            time_frame=time_frame,
            agriculture_filter=agriculture_filter,
            group=group,
            level_filter=level_filter,
            datetime=datetime,
            frequency=frequency,
            second_dropdown=second_dropdown,
            third_dropdown=third_dropdown,
        )
    else:
        raise ValueError("Invalid type specified. Use 'imports' or 'exports'.")
    
    context = {
        "hts_codes": hts_codes,
    }
    
    return graph.to_html(fullhtml=False, output_div=f"{type}_{level_filter}"), context


@router.get("/graph/product-hts/")
async def get_product_hts_graph(
    level: str,
    agriculture_filter: bool = False,
    group: bool = False,
    level_filter: str = "",
    time_frame: str = "",
    trade_type: str = "",
):
    graph, context = DataGraph(database_file="data/data.ddb").gen_hts_chart(
        level=level,
        agriculture_filter=agriculture_filter,
        group=group,
        level_filter=level_filter,
        frequency=time_frame,
        trade_type=trade_type,
    )
    return graph.to_html(), context


@router.get("/graph/product-ranking/")
async def get_hts_ranking_graph():
    graphs = DataGraph(database_file="data/data.ddb").gen_hts_ranking_chart()
    return {
        "export_top": graphs["export_top"].to_html(
            fullhtml=False, output_div="export_top"
        ),
        "export_bottom": graphs["export_bottom"].to_html(
            fullhtml=False, output_div="export_bottom"
        ),
        "import_top": graphs["import_top"].to_html(
            fullhtml=False, output_div="import_top"
        ),
        "import_bottom": graphs["import_bottom"].to_html(
            fullhtml=False, output_div="import_bottom"
        ),
    }


@router.get("/graph/naics/")
async def get_naics_graph(
    naics_code: str,
):
    graph, context = graphGenerator(database_file="data/data.ddb").gen_naics_graph(
        naics_code=naics_code,
    )
    return graph.to_html(), context


@router.get("/graph/indicadores/")
async def get_indicadores_graph(
    time_frame: str,
    column: str,
):
    graph, columns = IndexDataGraph(
        database_file="data/data.ddb"
    ).create_indicators_graph(
        time_frame=time_frame,
        column=column,
    )

    context = {
        "columns": columns,
    }

    return graph.to_html(), context


@router.get("/graph/consumer/")
async def get_consumer_graph(time_frame: str, column: str, data_type: str):
    graph, columns = IndexDataGraph(
        database_file="data/data.ddb"
    ).create_consumer_graph(time_frame=time_frame, column=column, data_type=data_type)

    context = {
        "columns": columns,
    }

    return graph.to_html(
        fullhtml=False, output_div=f"{data_type}_indices_consumidor"
    ), context


@router.get("/graph/energia/")
async def get_energy_graph(
    period: str = "monthly", metric: str = "generacion_neta_mkwh"
):
    graph, energy_metrics = IndexDataGraph(
        database_file="data/data.ddb"
    ).create_energy_chart(period=period, metric=metric)

    context = {
        "energy_metrics": energy_metrics,
    }

    return graph.to_html(fullhtml=False, output_div="energy"), context


@router.get("/graph/awards/category")
async def get_awards_category_graph(
    dropdown: int,
    second_dropdown: int,
    third_dropdown: str,
    time_frame: str,
):
    graph, categories = IndexDataGraph(
        database_file="data/data.ddb"
    ).create_spending_by_category_graph(
        year=dropdown,
        quarter=second_dropdown,
        month=second_dropdown,
        type=time_frame,
        category=third_dropdown,
    )

    context = {
        "categories": categories,
    }

    return graph.to_html(fullhtml=False, output_div="category"), context


@router.get("/graph/awards/secter")
async def get_awards_secter_graph(
    dropdown: str,
    time_frame: str,
):
    graph, agencies = IndexDataGraph(database_file="data/data.ddb").create_secter_graph(
        type=time_frame,
        secter=dropdown,
    )

    context = {
        "agencies": agencies,
    }

    return graph.to_html(fullhtml=False, output_div="secter"), context


@router.get("/graph/indices/precios")
async def get_indices_precios_graph(
    time_frame: str,
    data_type: str,
    column: str,
):
    graph, columns = IndexDataGraph(
        database_file="data/data.ddb"
    ).create_price_index_graph(
        time_frame=time_frame, data_type=data_type, column=column
    )

    context = {
        "columns_2": columns,
    }

    return graph.to_html(fullhtml=False, output_div="indices_precios"), context
