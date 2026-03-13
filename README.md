# 金融数据获取模块

> 零依赖、高可靠、易调用 - 专为AI助手设计的金融数据接口

## 概述

本模块提供A股、港股、大盘指数、资金流向等金融数据的获取能力。**不需要任何API Key，不需要安装任何第三方库**，只使用Python标准库。

## 安装

```bash
# 无需安装，直接使用
cd ~/.openclaw/workspace/financial-data
```

## 快速开始

### 方式一：直接运行测试

```bash
# 测试所有接口
python3 test_all.py

# 测试单个模块
python3 stocks.py
python3 index.py
python3 north_money.py
python3 news.py
python3 gainers.py
python3 announcements.py
python3 hkstocks.py
```

### 方式二：作为模块导入

```python
import sys
sys.path.append("/Users/xie/.openclaw/workspace/financial-data")

# 导入所有函数
from financial import *

# 获取A股实时行情
result = get_a_stocks()
print(result)

# 获取大盘指数
result = get_index_quotes()
print(result)

# 获取北向资金
result = get_north_money()
print(result)
```

## 函数清单

### 1. 行情数据 (stocks.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_realtime_quotes(secids)` | 获取指定股票行情 | `get_realtime_quotes(["1.600519"])` |
| `get_a_stocks()` | 获取A股自选股 | `get_a_stocks()` |
| `get_hk_stocks()` | 获取港股自选股 | `get_hk_stocks()` |
| `get_all_stocks()` | 获取全部自选股 | `get_all_stocks()` |

### 2. 大盘指数 (index.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_index_quotes(secids)` | 获取指数行情 | `get_index_quotes()` |
| `get_total_volume()` | 获取两市成交额 | `get_total_volume()` |

**常用指数代码：**
- `1.000001` = 上证指数
- `0.399001` = 深证成指
- `0.399006` = 创业板指

### 3. 北向资金 (north_money.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_north_money()` | 获取北向资金流向 | `get_north_money()` |
| `get_south_money()` | 获取南向资金流向 | `get_south_money()` |

### 4. 财经快讯 (news.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_cls_telegraph(count)` | 获取财联社电报 | `get_cls_telegraph(10)` |
| `get_important_news(count)` | 获取重要快讯(A级) | `get_important_news(10)` |

### 5. 涨跌幅榜 (gainers.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_top_gainers(count)` | 获取涨幅榜 | `get_top_gainers(10)` |
| `get_top_losers(count)` | 获取跌幅榜 | `get_top_losers(10)` |
| `get_top_volume(count)` | 获取成交量榜 | `get_top_volume(10)` |

### 6. 公告 (announcements.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_announcements(code, count)` | 获取公司公告 | `get_announcements("600519", 10)` |

### 7. 港股 (hkstocks.py)

| 函数 | 说明 | 示例 |
|------|------|------|
| `get_hk_quote(code)` | 获取单只港股 | `get_hk_quote("00700")` |
| `get_hk_quotes(codes)` | 获取多只港股 | `get_hk_quotes(["00700", "09988"])` |

## 返回格式

所有函数返回统一格式的字典：

```python
{
    "success": True/False,  # 是否成功
    "data": [...],           # 数据列表或详情
    "error": None 或 "错误信息"
}
```

## 错误处理

```python
result = get_a_stocks()

if result["success"]:
    for stock in result["data"]:
        print(f"{stock['name']}: {stock['price']}")
else:
    print(f"获取失败: {result['error']}")
```

## 数据源清单

| 数据类型 | 数据源 | 可靠性 |
|---------|--------|--------|
| A股实时行情 | 东方财富 push2 API | ✅ 稳定 |
| 港股实时 | 新浪财经 | ✅ 稳定 |
| 大盘指数 | 东方财富 push2 API | ✅ 稳定 |
| 涨跌幅榜 | 东方财富 push2 API | ✅ 稳定 |
| 北向资金 | 东方财富 kamt API | ✅ 稳定（盘后更准） |
| 财经快讯 | 财联社电报 | ✅ 稳定 |
| 公告 | 东方财富 | ✅ 稳定 |

## 维护说明

### 修改自选股

编辑 `stocks.py` 顶部的配置：

```python
A_STOCKS = [
    "1.600519",   # 贵州茅台
    "0.000858",   # 五粮液
    # ... 添加更多
]

HK_STOCKS = [
    "116.00700",  # 腾讯控股
    # ... 添加更多
]
```

### 代码格式说明

**A股代码格式：**
- 沪市：`1.{代码}`，如 `1.600519`
- 深市：`0.{代码}`，如 `0.000858`

**港股代码格式：**
- 港股：`116.{代码}`，如 `116.00700`
- 或直接用 `hkstocks` 模块：`"00700"`

## 注意事项

1. **北向资金**：盘中数据可能有几分钟延迟，建议盘后使用
2. **港股**：部分字段可能为空
3. **频率限制**：东方财富接口无明确限制，但建议间隔>1秒
4. **网络问题**：如遇超时，检查网络后重试

---

**创建时间**: 2026-03-13  
**维护者**: 阿肝
