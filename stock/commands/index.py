from __future__ import annotations

import click

from ..api.baidu import fetch_chgdiagram_payload
from ..api.qq import fetch_pt_board_rank_payload, get_stock_by_query, zdf_percent

CODES = {
    'ab': [
        'sh000001',
        'sz399001',
        'sz399006',
        'sh000688',
        'sh000300',
        'sh000905',
        'sh000852',
        'bj899050',
    ],
    'us': [
        'us.DJI',
        'us.IXIC',
        'us.INX',
    ],
    'hk': [
        'r_hkHSI',
        'r_hkHSCEI',
        'r_hkHSTECH',
    ],
}


def format_quotes_markdown(quotes: list[dict]) -> str:
    lines = []
    for quote in quotes:
        lines.append(
            ",".join(
                [
                    quote["code"],
                    quote["name"],
                    quote["price"],
                    quote["change_rate"],
                    quote["previous_close"],
                    quote["open"],
                    quote["high"],
                    quote["low"],
                ]
            )
        )
    return "\n".join(
        [
            "## 指数",
            "",
            "```csv",
            "代码,名称,价格,涨跌幅,昨收价,开盘价,最高价,最低价",
            *lines,
            "```",
        ]
    )


def _format_status(status: str) -> str:
    if status == "up":
        return "上涨"
    if status == "same":
        return "平盘"
    if status == "down":
        return "下跌"
    return status


def get_chgdiagram_data(market: str) -> dict:
    payload = fetch_chgdiagram_payload(market)
    result = payload.get("Result") if isinstance(payload, dict) else {}
    chg = result.get("chgdiagram") if isinstance(result, dict) else {}
    ratio = chg.get("ratio") if isinstance(chg, dict) else {}
    diagram = chg.get("diagram") if isinstance(chg, dict) else []
    up = int(ratio.get("up", 0)) if isinstance(ratio, dict) else 0
    balance = int(ratio.get("balance", 0)) if isinstance(ratio, dict) else 0
    down = int(ratio.get("down", 0)) if isinstance(ratio, dict) else 0
    items: list[dict] = []
    if isinstance(diagram, list):
        for item in diagram:
            if not isinstance(item, dict):
                continue
            items.append(
                {
                    "status": str(item.get("status", "")),
                    "title": str(item.get("title", "")),
                    "count": int(item.get("count", 0) or 0),
                }
            )
    return {"ratio": {"up": up, "balance": balance, "down": down}, "diagram": items}


def format_chgdiagram_markdown(data: dict) -> str:
    ratio = data.get("ratio", {})
    diagram = data.get("diagram", [])
    lines = [
        f"{_format_status(str(item.get('status', '')))},{str(item.get('title', ''))},{int(item.get('count', 0))}"
        for item in diagram
        if isinstance(item, dict)
    ]
    return "\n".join(
        [
            "## 涨跌分布",
            "",
            f"上涨：{ratio.get('up', 0)}家，平盘：{ratio.get('balance', 0)}家，下跌：{ratio.get('down', 0)}家",
            "",
            "```csv",
            "状态,区间,数量",
            *lines,
            "```",
        ]
    )


def get_pt_board_rank_list(sort: str, direct: str, offset: int, count: int) -> dict:
    payload = fetch_pt_board_rank_payload(
        board_type="hy",
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
                    "zd": str(it.get("zd", "")),
                    "hsl": str(it.get("hsl", "")),
                    "lb": str(it.get("lb", "")),
                    "ltsz": str(it.get("ltsz", "")),
                    "zljlr": str(it.get("zljlr", "")),
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
                it.get("zd", ""),
                it.get("hsl", ""),
                it.get("lb", ""),
                it.get("ltsz", ""),
                it.get("zljlr", ""),
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
            "## 行业板块",
            "",
            "```csv",
            "代码,名称,涨跌幅,5日涨跌,涨跌额,换手率,量比,流通市值,主力净流入,领涨股票代码,领涨股票,领涨股涨跌",
            *lines,
            "```",
        ]
    )


@click.command(name="index")
@click.option(
    "--market",
    default="ab",
    show_default=True,
    type=click.Choice(["ab", "us", "hk"], case_sensitive=False),
    help="市场",
)
def index(market: str):
    """大盘指数行情"""
    market = market.lower()
    data = get_stock_by_query(','.join(CODES[market]))
    click.echo("# 大盘行情")
    click.echo("")
    click.echo(format_quotes_markdown(data))
    click.echo("")
    chgdiagram_data = get_chgdiagram_data(market)
    click.echo(format_chgdiagram_markdown(chgdiagram_data))
    if market == "ab":
        click.echo("")
        pt_data = get_pt_board_rank_list("priceRatio", "down", 0, 30)
        click.echo(format_pt_rank_table(pt_data))
