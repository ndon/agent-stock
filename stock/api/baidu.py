from __future__ import annotations

import click
import requests

from . import http_get_with_proxy_fallback


def fetch_latest_news_payload(market: str, code: str) -> dict:
    url = "https://finance.pae.baidu.com/vapi/sentimentlist"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={
                "market": market,
                "code": code,
                "query": code,
                "financeType": "stock",
                "benefitType": "",
                "pn": "0",
                "rn": "20",
                "finClientType": "pc",
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gushitong.baidu.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"资讯接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"资讯接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("资讯接口返回解析失败") from exc


def fetch_fundflow_day_payload(market: str, code: str, date: str) -> dict:
    url = "https://finance.pae.baidu.com/vapi/v1/fundflow"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={
                "finance_type": "stock",
                "fund_flow_type": "day",
                "market": market,
                "code": code,
                "date": date,
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gushitong.baidu.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"资金流向接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"资金流向接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("资金流向接口返回解析失败") from exc


def fetch_fundflow_spread_payload(market: str, code: str) -> dict:
    url = "https://finance.pae.baidu.com/vapi/v1/fundflow"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={
                "finance_type": "stock",
                "fund_flow_type": "",
                "market": market,
                "code": code,
                "type": "stock",
                "finClientType": "pc",
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gushitong.baidu.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"资金流向接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"资金流向接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("资金流向接口返回解析失败") from exc
