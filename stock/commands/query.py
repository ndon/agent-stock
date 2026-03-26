from __future__ import annotations

import click

from ..api.eastmoney import fetch_stock_select_payload
from ..api.qq import zdf_percent


def get_select_results(keyword: str, page_size: int = 50, page_no: int = 1) -> list[dict]:
    payload = fetch_stock_select_payload(keyword, page_size, page_no)
    data_obj = payload.get("data", {}).get("result", {}) if isinstance(payload, dict) else {}
    items = data_obj.get("dataList", []) if isinstance(data_obj, dict) else []
    results: list[dict] = []
    if isinstance(items, list):
        for it in items:
            if not isinstance(it, dict):
                continue
            market_short = str(it.get("MARKET_SHORT_NAME", "")).strip()
            security_code = str(it.get("SECURITY_CODE", "")).strip()
            results.append({
                "symbol": f"{market_short.lower()}{security_code}",
                "code": security_code,
                "name": str(it.get("SECURITY_SHORT_NAME", "")).strip(),
                "price": str(it.get("NEWEST_PRICE", "")),
                "change_rate": zdf_percent(str(it.get("CHG", ""))),
                "pb": str(it.get("PB", "")),
                "pe": str(it.get("PE_DYNAMIC", "")),
                "circulation_market_value": str(it.get("CIRCULATION_MARKET_VALUE<140>", "")),
                "volume": str(it.get("VOLUME", "")),
                "turnover": str(it.get("TURNOVER_RATE", "")),
                "trading_volumes": str(it.get("TRADING_VOLUMES", "")),
            })
    return results


def format_select_table(results: list[dict]) -> str:
    if not results:
        return "暂无数据"
    lines = ["代码,名称,现价,涨跌幅,市盈率,市净率,流通市值,成交量,换手率,成交额"]
    for r in results:
        lines.append(
            ",".join(
                [
                    r.get("code", ""),
                    r.get("name", ""),
                    r.get("price", ""),
                    r.get("change_rate", ""),
                    r.get("pe", ""),
                    r.get("pb", ""),
                    r.get("circulation_market_value", ""),
                    r.get("volume", ""),
                    r.get("turnover", ""),
                    r.get("trading_volumes", ""),
                ]
            )
        )
    return "\n".join(["```csv", *lines, "```"])


@click.command(name="query")
@click.argument("keyword")
@click.option("--page-size", default=50, show_default=True, type=click.IntRange(1, 100), help="每页数量")
@click.option("--page-no", default=1, show_default=True, type=click.IntRange(1, 100), help="页码")
def query(keyword: str, page_size: int, page_no: int):
    """条件选股"""
    data = get_select_results(keyword, page_size, page_no)
    click.echo(format_select_table(data))
