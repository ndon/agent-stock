# agent-stock

[![CI](https://github.com/AnoyiX/agent-stock/actions/workflows/ci.yml/badge.svg)](https://github.com/AnoyiX/agent-stock/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/agent-stock.svg)](https://pypi.org/project/agent-stock/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](https://pypi.org/project/agent-stock/)

股市数据命令行工具，支持市场、个股等数据。

## 安装

```bash
# pipx（推荐）
pipx install agent-stock

# uv tool
uv tool install agent-stock

# pip（虚拟环境或本地环境）
python -m pip install agent-stock
```

升级到最新版本：

```bash
pipx upgrade agent-stock
uv tool upgrade agent-stock
python -m pip install -U agent-stock
```

## 快速开始

```bash
# 常用
stock quote 000001
stock plate 000001
stock news 000001

# 技术分析与市场
stock kline 000001 --count 60
stock fundflow 000001
stock chgdiagram --market ab
stock heatmap --market ab

# 帮助与版本
stock --help
stock quote --help
stock -v
```

## 命令总览

### 全局选项

| 选项           | 类型/范围     | 默认值 | 说明                     |
| -------------- | ------------- | ------ | ------------------------ |
| -v, --version  | —             | —      | 显示版本信息             |
| -d, --verbose  | Flag          | —      | 启用调试日志             |
| -i, --interval | 整数 [1,3600] | 10     | dashboard 刷新间隔（秒） |
| --no-color     | Flag          | —      | 禁用颜色输出             |

### 市场相关的命令

| 命令        | 参数      | 选项                           | 说明                                            |
| ----------- | --------- | ------------------------------ | ----------------------------------------------- |
| market      | —         | —                              | 查看大盘指数总览（占位）                        |
| search      | KEYWORD   | —                              | 按名称/关键词搜索（输出 CSV）                   |
| chgdiagram  | —         | --market <ab/us/hk>（默认 ab） | 涨跌分布统计                                    |
| heatmap     | —         | --market <ab/us/hk>（默认 ab） | 行业板块热力图                                  |
| config show | —         | —                              | 查看当前配置                                    |
| config set  | key value | —                              | 设置配置项（仅支持 market: US&#124;CN&#124;HK） |

### 个股相关的命令

| 命令     | 参数   | 选项                        | 说明                              |
| -------- | ------ | --------------------------- | --------------------------------- |
| quote    | SYMBOL | —                           | 查询个股实时报价与指标            |
| plate    | SYMBOL | —                           | 查看地域/行业/概念相关板块涨跌幅  |
| news     | SYMBOL | —                           | 查看个股最新资讯摘要              |
| kline    | SYMBOL | --count N（1..90，默认 45） | 输出最近 N 条日 K 与常用技术指标  |
| fundflow | SYMBOL | —                           | 查看资金分布、每日主力/散户净流向 |

## 配置

```bash
# 查看当前配置
stock config show

# 设置市场（US | CN | HK）
stock config set market US
```

## 开发

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest tests/ -v

# Lint
uv run ruff check .

# 安装当前目录源码，并暴露 `stock` 命令
uv tool install --from . agent-stock

# 强制升级
uv tool install --from . agent-stock --force --reinstall --refresh --no-cache

# 卸载
uv tool uninstall agent-stock

# 调试
uv run python -m stock quote 000001
uv run python -m stock plate 000001
uv run python -m stock news 000001
```

## License

Apache-2.0
