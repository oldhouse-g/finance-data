#!/usr/bin/env python3
"""
金融数据模块 - 全部接口测试

运行方式: python3 test_all.py
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stocks import get_a_stocks, get_hk_stocks
from index import get_index_quotes, get_total_volume
from north_money import get_north_money, get_south_money
from news import get_cls_telegraph, get_important_news
from gainers import get_top_gainers, get_top_losers
from announcements import get_announcements
from hkstocks import get_hk_quotes


def test_section(title):
    """打印测试标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_result(name, result):
    """打印测试结果"""
    if result["success"]:
        data = result.get("data")
        if data is None:
            print(f"  {name}: ⚠️ {result.get('error', '无数据')}")
        elif isinstance(data, list):
            print(f"  {name}: ✅ 成功 ({len(data)}条)")
            # 打印前3条
            for i, item in enumerate(data[:3]):
                if isinstance(item, dict):
                    name_field = item.get("name", item.get("title", ""))
                    print(f"      {i+1}. {name_field}")
                else:
                    print(f"      {i+1}. {item}")
        elif isinstance(data, dict):
            print(f"  {name}: ✅ 成功")
            # 打印关键字段
            for k, v in list(data.items())[:5]:
                if isinstance(v, float):
                    print(f"      {k}: {v:+.2f}" if abs(v) < 1000 else f"      {k}: {v:,.0f}")
                else:
                    print(f"      {k}: {v}")
        else:
            print(f"  {name}: ✅ 成功")
    else:
        print(f"  {name}: ❌ 失败 - {result['error']}")


def main():
    print("🧪 金融数据模块 - 全部接口测试")
    print(f"⏰ 时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 行情数据
    test_section("1. A股自选股行情")
    test_result("get_a_stocks", get_a_stocks())
    
    test_section("2. 港股自选股行情")
    test_result("get_hk_stocks", get_hk_stocks())
    
    # 2. 大盘指数
    test_section("3. 大盘指数")
    test_result("get_index_quotes", get_index_quotes())
    test_result("get_total_volume", get_total_volume())
    
    # 3. 北向资金
    test_section("4. 北向资金")
    test_result("get_north_money", get_north_money())
    test_result("get_south_money", get_south_money())
    
    # 4. 财经快讯
    test_section("5. 财经快讯")
    test_result("get_cls_telegraph", get_cls_telegraph(10))
    test_result("get_important_news", get_important_news(5))
    
    # 5. 涨跌幅榜
    test_section("6. 涨跌幅榜")
    test_result("get_top_gainers", get_top_gainers(5))
    test_result("get_top_losers", get_top_losers(5))
    
    # 6. 公告
    test_section("7. 上市公司公告")
    test_result("get_announcements", get_announcements("600519", 5))
    
    # 7. 港股单独测试
    test_section("8. 港股实时(新浪)")
    test_result("get_hk_quotes", get_hk_quotes(["00700", "09988", "01810"]))
    
    # 完成
    print("\n" + "=" * 60)
    print("  ✅ 全部测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
