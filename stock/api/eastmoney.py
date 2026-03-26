import click
import requests


def fetch_stock_select_payload(keyword: str, page_size: int = 50, page_no: int = 1) -> dict:
    url = "https://np-tjxg.eastmoney.com/api/smart-tag/stock/v3/pw/search-code"
    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "keyWord": keyword,
                "pageSize": page_size,
                "pageNo": page_no,
                "fingerprint": "512bd9beaf2fcd06b7972fb94d97873f",
                "gids": [],
                "removedConditionIdList": [],
                "timestamp": str(int(__import__("time").time() * 1000)),
                "shareToGuba": False,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        raise click.ClickException(f"条件选股接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"条件选股接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("条件选股接口返回解析失败") from exc
