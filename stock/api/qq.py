from __future__ import annotations

import json

import click
import requests

from . import http_get_with_proxy_fallback


def fetch_quote_json(query_code: str) -> dict:
    url = "https://sqt.gtimg.cn"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={"q": query_code, "fmt": "json"},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gu.qq.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        text = response.content.decode("gbk", errors="ignore")
        payload = json.loads(text)
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"行情接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"行情接口不可用: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise click.ClickException("行情接口返回解析失败") from exc


def fetch_kline_payload(query_code: str) -> dict:
    url = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={"param": f"{query_code},day,,,90,qfq"},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gu.qq.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"日K接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"日K接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("日K接口返回解析失败") from exc


def fetch_plate_payload(code: str) -> dict:
    url = "https://proxy.finance.qq.com/ifzqgtimg/appstock/app/stockinfo/plateNew"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={"code": code, "app": "wzq", "zdf": "1"},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gu.qq.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"板块接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"板块接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("板块接口返回解析失败") from exc


def fetch_search_payload(query: str) -> dict:
    url = "https://proxy.finance.qq.com/cgi/cgi-bin/smartbox/search"
    try:
        response = http_get_with_proxy_fallback(
            url,
            params={"stockFlag": "1", "fundFlag": "1", "app": "official_website", "query": query},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://gu.qq.com/",
                "Accept": "application/json,text/plain,*/*",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
        return payload
    except requests.HTTPError as exc:
        raise click.ClickException(f"搜索接口请求失败: HTTP {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise click.ClickException(f"搜索接口不可用: {exc}") from exc
    except ValueError as exc:
        raise click.ClickException("搜索接口返回解析失败") from exc
