from __future__ import annotations

import click

from ..api.qq import fetch_pt_board_rank_payload, zdf_percent


def get_pt_board_rank_list(sort: str, direct: str, offset: int, count: int) -> dict:
    payload = fetch_pt_board_rank_payload(
        board_type="hy2",
        sort_type=sort,
        direct=direct,
        offset=offset,
        count=count,
    )
    data_obj = payload.get("data") if isinstance(payload, dict) else {}
    rank_list = data_obj.get("rank_list") if isinstance(data_obj, dict) else []
    items: list[dict] = []
    if isinstance(rank_list, list):
        for it in rank_list:
            if not isinstance(it, dict):
                continue
            lzg = it.get("lzg") or {}
            items.append(
                {
                    "code": str(it.get("code", "").replace("pt", "")),
                    "name": str(it.get("name", "")),
                    "zdf": zdf_percent(str(it.get("zdf", ""))),
                    "zdf_d5": zdf_percent(str(it.get("zdf_d5", ""))),
                    "zdf_d20": zdf_percent(str(it.get("zdf_d20", ""))),
                    "zdf_d60": zdf_percent(str(it.get("zdf_d60", ""))),
                    "zdf_w52": zdf_percent(str(it.get("zdf_w52", ""))),
                    "zdf_y": zdf_percent(str(it.get("zdf_y", ""))),
                    "zxj": str(it.get("zxj", "")),
                    "zd": str(it.get("zd", "")),
                    "turnover": str(it.get("turnover", "")),
                    "hsl": str(it.get("hsl", "")),
                    "lb": str(it.get("lb", "")),
                    "zsz": str(it.get("zsz", "")),
                    "ltsz": str(it.get("ltsz", "")),
                    "zljlr": str(it.get("zljlr", "")),
                    "zljlr_d5": str(it.get("zljlr_d5", "")),
                    "zljlr_d20": str(it.get("zljlr_d20", "")),
                    "zllc": str(it.get("zllc", "")),
                    "zllr": str(it.get("zllr", "")),
                    "lzg_code": str(lzg.get("code", "")),
                    "lzg_name": str(lzg.get("name", "")),
                    "lzg_zdf": zdf_percent(str(lzg.get("zdf", ""))),
                }
            )
    return {"offset": int(data_obj.get("offset", 0) or 0), "total": int(data_obj.get("total", 0) or 0), "items": items}


def format_pt_rank_table(data: dict) -> str:
    items = data.get("items", [])
    if not items:
        return "暂无数据"
    lines = [
        ",".join(
            [
                it.get("code", ""),
                it.get("name", ""),
                it.get("zdf", ""),
                it.get("zdf_d5", ""),
                it.get("zdf_d20", ""),
                it.get("zxj", ""),
                it.get("zd", ""),
                it.get("turnover", ""),
                it.get("hsl", ""),
                it.get("lb", ""),
                it.get("zsz", ""),
                it.get("ltsz", ""),
                it.get("zljlr", ""),
                it.get("zljlr_d5", ""),
                it.get("zljlr_d20", ""),
                it.get("lzg_code", ""),
                it.get("lzg_name", ""),
                it.get("lzg_zdf", ""),
            ]
        )
        for it in items
        if isinstance(it, dict)
    ]
    return "\n".join(
        [
            "```csv",
            "代码,名称,涨跌幅,5日涨跌,20日涨跌,最新价,涨跌额,成交额,换手率,量比,总市值,流通市值,主力净流入,5日主力净流入,20日主力净流入,领涨股票代码,领涨股票,领涨股涨跌",
            *lines,
            "```",
        ]
    )


@click.command(name="pt")
@click.option(
    "--sort",
    default="priceRatio",
    show_default=True,
    help="排序类型(price/priceRatio/priceRatioD5/priceRatioD20/priceRatioD60/priceRatioW52/priceRatioY)",
)
@click.option(
    "--direct",
    default="down",
    show_default=True,
    type=click.Choice(["down", "up"], case_sensitive=False),
    help="排序方向",
)
@click.option("--offset", default=0, show_default=True, type=click.IntRange(0, 100000), help="偏移量")
@click.option("--count", default=30, show_default=True, type=click.IntRange(1, 100), help="数量")
def pt(sort: str, direct: str, offset: int, count: int):
    """申万行业板块排序（限A股）"""
    data = get_pt_board_rank_list(sort, direct, offset, count)
    click.echo(format_pt_rank_table(data))
