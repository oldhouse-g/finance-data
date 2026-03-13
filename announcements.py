"""
金融数据获取模块 - 上市公司公告

【使用说明】
本模块提供A股上市公司公告查询。

【数据来源】
- 东方财富公告API

【使用示例】
>>> from announcements import get_announcements
>>> result = get_announcements("600519")
>>> for ann in result["data"]:
>>>     print(f"{ann['title']}")
"""

import urllib.request
import json
from datetime import datetime


def get_announcements(stock_code=None, count=10):
    """
    获取上市公司公告
    
    【参数】
        stock_code: str - 股票代码（可选），如 "600519"
                           不填则获取全市场公告
        count: int - 返回条数，默认10
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "title": "贵州茅台关于XXX的公告",
                    "stock_code": "600519",
                    "stock_name": "贵州茅台",
                    "ann_time": "2025-11-08",
                    "url": "https://www.eastmoney.com/..."
                },
                ...
            ],
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    """
    # 股票代码格式处理
    f_node = "0"  # 默认沪市
    if stock_code:
        if stock_code.startswith("0"):
            f_node = "1"  # 深市
        elif stock_code.startswith("3"):
            f_node = "1"  # 创业板
    
    url = f"https://np-anotice-stock.eastmoney.com/api/security/ann?sr=-1&page_size={count}&page_index=1&ann_type=SHA&client_source=web&f_node={f_node}"
    
    if stock_code:
        url += f"&stock={stock_code}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if not data.get("data") or not data["data"].get("list"):
            return {"success": False, "data": None, "error": "无公告数据", "source": None}
        
        result = []
        for item in data["data"]["list"]:
            # 解析时间
            time_str = ""
            if item.get("ann_time"):
                try:
                    dt = datetime.strptime(str(item["ann_time"])[:8], "%Y%m%d")
                    time_str = dt.strftime("%Y-%m-%d")
                except:
                    time_str = str(item.get("ann_time", ""))
            
            result.append({
                "title": item.get("title", ""),
                "stock_code": item.get("stock_code", stock_code or ""),
                "stock_name": item.get("stock_name", ""),
                "ann_time": time_str,
                "url": f"https://www.eastmoney.com/zongyi.html?code={item.get('stock_code', '')}"
            })
        
        return {"success": True, "data": result, "error": None, "source": "东方财富公告 API (第一层)"}
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e), "source": None}


# ==================== 独立运行测试 ====================
if __name__ == "__main__":
    print("=" * 50)
    print("测试最新公告")
    print("=" * 50)
    
    result = get_announcements(count=10)
    if result["success"]:
        for ann in result["data"]:
            print(f"[{ann['ann_time']}] {ann['stock_name']} - {ann['title'][:40]}...")
    else:
        print(f"错误: {result['error']}")
