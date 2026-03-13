"""
金融数据获取模块 - 统一入口

【快速开始】
>>> from financial import get_daily_briefing
>>> result = get_daily_briefing()
>>> print(result)

【模块列表】
- stocks: A股/港股实时行情
- index: 大盘指数
- north_money: 北向资金
- news: 财经快讯
- gainers: 涨跌幅榜
- announcements: 上市公司公告
- hkstocks: 港股实时行情

【详细文档】
请阅读 README.md
"""

from .stocks import get_realtime_quotes, get_a_stocks, get_hk_stocks, get_all_stocks
from .index import get_index_quotes, get_total_volume
from .north_money import get_north_money, get_south_money
from .news import get_cls_telegraph, get_important_news
from .gainers import get_top_gainers, get_top_losers
from .announcements import get_announcements
from .hkstocks import get_hk_quote, get_hk_quotes


__all__ = [
    # 行情
    "get_realtime_quotes",
    "get_a_stocks", 
    "get_hk_stocks",
    "get_all_stocks",
    # 指数
    "get_index_quotes",
    "get_total_volume",
    # 资金
    "get_north_money",
    "get_south_money",
    # 新闻
    "get_cls_telegraph",
    "get_important_news",
    # 排行榜
    "get_top_gainers",
    "get_top_losers",
    # 公告
    "get_announcements",
    # 港股
    "get_hk_quote",
    "get_hk_quotes",
]
