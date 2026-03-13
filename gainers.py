"""
金融数据获取模块 - 涨跌幅榜

【使用说明】
本模块提供A股涨跌幅排行榜查询。

【参数说明】
- po=1: 降序（涨幅榜从大到小）
- po=0: 升序（跌幅榜从小到大）
- pn: 页码，从1开始
- pz: 每页数量

【使用示例】
>>> from gainers import get_top_gainers
>>> result = get_top_gainers(10)
>>> for stock in result["data"]:
>>>     print(f"{stock['name']} {stock['change_pct']:+6.2f}%")
"""

import urllib.request
import json


def get_top_gainers(count=10, page=1):
    """
    获取涨幅榜
    
    【参数】
        count: int - 返回条数，默认10，最大50
        page: int - 页码，默认1
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "code": "600519",
                    "name": "贵州茅台",
                    "price": 1392.00,
                    "change_pct": 5.23,
                    "change_amt": 69.12,
                    "volume": 123456,     # 成交量(手)
                    "amount": 12345678,  # 成交额(元)
                    "high": 1400.00,      # 最高
                    "low": 1320.00,       # 最低
                    "open": 1325.00,      # 今开
                    "prev_close": 1310.00 # 昨收
                },
                ...
            ],
            "error": None
        }
    """
    return _get_ranklist(po=1, count=count, page=page)


def get_top_losers(count=10, page=1):
    """
    获取跌幅榜
    
    【参数】
        count: int - 返回条数，默认10，最大50
        page: int - 页码，默认1
    
    【返回】
        同 get_top_gainers
    """
    return _get_ranklist(po=0, count=count, page=page)


def get_top_volume(count=10, page=1):
    """
    获取成交量榜（换手率最高）
    
    【参数】
        count: int - 返回条数，默认10，最大50
        page: int - 页码，默认1
    
    【返回】
        同 get_top_gainers
    """
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn={page}&pz={count}&po=1&np=1&fltt=2&invt=2&fid=f5&fs=m:1+t:2,m:1+t:23,m:0+t:6,m:0+t:13,m:0+t:80&fields=f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18"
    
    return _fetch_ranklist(url)


def _get_ranklist(po=1, count=10, page=1):
    """
    获取排行榜通用方法
    
    【参数】
        po: int - 排序方向，1=降序，0=升序
        count: int - 每页条数
        page: int - 页码
    """
    # po=1 涨幅榜, fid=f3 (涨跌幅)
    # po=0 跌幅榜
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn={page}&pz={count}&po={po}&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23,m:0+t:6,m:0+t:13,m:0+t:80&fields=f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18"
    
    return _fetch_ranklist(url)


def _fetch_ranklist(url):
    """获取排行榜数据"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if not data.get("data") or not data["data"].get("diff"):
            return {"success": False, "data": None, "error": "无数据"}
        
        result = []
        for item in data["data"]["diff"]:
            result.append({
                "code": item.get("f12", ""),
                "name": item.get("f14", ""),
                "price": _safe_float(item.get("f2")),
                "change_pct": _safe_float(item.get("f3")),
                "change_amt": _safe_float(item.get("f4")),
                "volume": _safe_int(item.get("f5")),
                "amount": _safe_int(item.get("f6")),
                "high": _safe_float(item.get("f15")),
                "low": _safe_float(item.get("f16")),
                "open": _safe_float(item.get("f17")),
                "prev_close": _safe_float(item.get("f18")),
            })
        
        return {"success": True, "data": result, "error": None}
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def _safe_float(val):
    """安全转换为浮点数"""
    if val is None or val == "-" or val == "":
        return 0.0
    try:
        return float(val)
    except:
        return 0.0


def _safe_int(val):
    """安全转换为整数"""
    if val is None or val == "-" or val == "":
        return 0
    try:
        return int(float(val))
    except:
        return 0


# ==================== 独立运行测试 ====================
if __name__ == "__main__":
    print("=" * 50)
    print("测试涨幅榜 Top 10")
    print("=" * 50)
    
    result = get_top_gainers(10)
    if result["success"]:
        for i, stock in enumerate(result["data"], 1):
            print(f"{i:2d}. {stock['name']:10s} {stock['price']:8.2f} {stock['change_pct']:+6.2f}%")
    else:
        print(f"错误: {result['error']}")
    
    print("\n" + "=" * 50)
    print("测试跌幅榜 Top 10")
    print("=" * 50)
    
    result = get_top_losers(10)
    if result["success"]:
        for i, stock in enumerate(result["data"], 1):
            print(f"{i:2d}. {stock['name']:10s} {stock['price']:8.2f} {stock['change_pct']:+6.2f}%")
    else:
        print(f"错误: {result['error']}")
