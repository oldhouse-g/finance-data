"""
金融数据获取模块 - 大盘指数

【使用说明】
本模块提供A股主要指数的实时行情查询。

【指数代码】
- 1.000001 = 上证指数
- 0.399001 = 深证成指
- 0.399006 = 创业板指
- 1.000300 = 沪深300
- 1.000016 = 上证50
- 0.399673 = 创业板50

【使用示例】
>>> from index import get_index_quotes
>>> result = get_index_quotes()
>>> print(result["data"])
"""

import urllib.request
import json


# 常用指数配置
INDEX_LIST = [
    ("1.000001", "上证指数"),
    ("0.399001", "深证成指"),
    ("0.399006", "创业板指"),
    ("1.000300", "沪深300"),
    ("1.000016", "上证50"),
]


def get_index_quotes(secids=None):
    """
    获取大盘指数行情
    
    【参数】
        secids: list - 指数代码列表，默认为常用指数
                示例: ["1.000001", "0.399001", "0.399006"]
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "code": "000001",
                    "name": "上证指数",
                    "price": 4129.10,
                    "change_pct": -0.10,
                    "change_amt": -4.15,
                    "volume": 1234567890,   # 成交量(手)
                    "amount": 108000000000, # 成交额(元)
                    "high": 4150.00,        # 最高
                    "low": 4120.00,         # 最低
                    "open": 4133.25,        # 今开
                    "prev_close": 4133.25   # 昨收
                },
                ...
            ],
            "error": None 或错误信息
        }
    """
    if secids is None:
        secids = [code for code, _ in INDEX_LIST]
    
    if not secids:
        return {"success": False, "data": None, "error": "secids不能为空"}
    
    # 拼接代码
    secids_str = ",".join(secids)
    
    # 请求URL (使用完整字段)
    url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f1,f2,f3,f4,f5,f6,f12,f14,f15,f16,f17,f18&secids={secids_str}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if data.get("data") and data["data"].get("diff"):
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
        else:
            return {"success": False, "data": None, "error": "未获取到数据"}
            
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_total_volume():
    """
    获取沪深两市总成交额
    
    【返回】
        dict: {
            "success": True/False,
            "data": {
                "sh_amount": 108000000000,   # 沪市成交额(元)
                "sz_amount": 136000000000,   # 深市成交额(元)
                "total_amount": 244000000000, # 两市合计(元)
                "sh_volume": 108000000,      # 沪市成交量(手)
                "sz_volume": 136000000       # 深市成交量(手)
            },
            "error": None
        }
    """
    # 同时获取上证和深证的成交额
    result = get_index_quotes(["1.000001", "0.399001"])
    
    if result["success"] and result["data"]:
        sh_amount = 0
        sz_amount = 0
        sh_volume = 0
        sz_volume = 0
        
        for item in result["data"]:
            if item["code"] == "000001":  # 上证
                sh_amount = item.get("amount", 0)
                sh_volume = item.get("volume", 0)
            elif item["code"] == "399001":  # 深证
                sz_amount = item.get("amount", 0)
                sz_volume = item.get("volume", 0)
        
        return {
            "success": True,
            "data": {
                "sh_amount": sh_amount,
                "sz_amount": sz_amount,
                "total_amount": sh_amount + sz_amount,
                "sh_volume": sh_volume,
                "sz_volume": sz_volume
            },
            "error": None
        }
    else:
        return {"success": False, "data": None, "error": result.get("error")}


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
    print("测试大盘指数行情")
    print("=" * 50)
    
    result = get_index_quotes()
    if result["success"]:
        for idx in result["data"]:
            vol = idx.get("amount", 0)
            vol_wan = vol / 100000000 if vol else 0
            print(f"{idx['name']:8s} {idx['price']:8.2f} {idx['change_pct']:+6.2f}% 成交:{vol_wan:,.0f}亿")
    else:
        print(f"错误: {result['error']}")
    
    print("\n" + "=" * 50)
    print("测试两市总成交额")
    print("=" * 50)
    
    result = get_total_volume()
    if result["success"]:
        total = result["data"]["total_amount"] / 100000000
        print(f"沪市: {result['data']['sh_amount']/100000000:,.0f}亿")
        print(f"深市: {result['data']['sz_amount']/100000000:,.0f}亿")
        print(f"合计: {total:,.0f}亿")
    else:
        print(f"错误: {result['error']}")
