"""
金融数据获取模块 - A股/港股实时行情

【使用说明】
本模块提供A股和港股的实时行情查询功能。

【secids格式说明】
- A股沪市：1.{代码}，如 1.600519 = 贵州茅台
- A股深市：0.{代码}，如 0.000858 = 五粮液
- 港股：116.{代码}，如 116.00700 = 腾讯控股

【返回值格式】
{
    "success": true/false,
    "data": [...] 或 null,
    "error": "错误信息" 或 null,
    "source": "数据来源说明"
}

【使用示例】
>>> from stocks import get_realtime_quotes
>>> result = get_realtime_quotes(["1.600519", "116.00700"])
>>> print(result["data"])
"""

import urllib.request
import json


# ==================== 蟹大爷自选股配置 ====================
# 如需修改自选股，编辑此配置
A_STOCKS = [
    "1.600519",   # 贵州茅台
    "0.000858",   # 五粮液
    "0.000333",   # 美的集团
    "1.600887",   # 伊利股份
    "1.600036",   # 招商银行
    "0.000001",   # 平安银行
]

HK_STOCKS = [
    "116.00700",  # 腾讯控股
    "116.09988",  # 阿里巴巴-W
    "116.01810",  # 小米集团-W
    "116.01024",  # 联想集团
]

# 全部自选股
ALL_STOCKS = A_STOCKS + HK_STOCKS


def get_realtime_quotes(secids):
    """
    获取A股/港股实时行情
    
    【参数】
        secids: list - 证券代码列表
                示例: ["1.600519", "0.000858", "116.00700"]
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "code": "600519",
                    "name": "贵州茅台",
                    "price": 1392.00,
                    "change_pct": -0.57,
                    "change_amt": -7.96,
                    "volume": 123456789,     # 成交量(手)
                    "amount": 1234567890,    # 成交额(元)
                    "high": 1400.00,         # 最高
                    "low": 1385.00,          # 最低
                    "open": 1395.00,         # 今开
                    "prev_close": 1399.96,  # 昨收
                    "market": "SH"          # 市场: SH=上海, SZ=深圳, HK=港股
                },
                ...
            ],
            "error": None 或错误信息
        }
    
    【字段说明】
        - f2=最新价, f3=涨跌幅(%), f4=涨跌额
        - f5=成交量(手), f6=成交额(元)
        - f15=最高, f16=最低, f17=今开, f18=昨收
    
    【注意】
        - 港股只有部分字段(price, change_pct, change_amt, name)
        - 指数使用此接口时fields不同，详见index.py
    """
    if not secids:
        return {"success": False, "data": None, "error": "secids不能为空"}
    
    # 拼接代码
    secids_str = ",".join(secids)
    
    # 请求URL
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
                # 判断市场
                code = item.get("f12", "")
                if code.startswith("0") and len(code) == 6:
                    market = "SZ"
                elif code.startswith("6") and len(code) == 6:
                    market = "SH"
                else:
                    market = "HK"
                
                result.append({
                    "code": code,
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
                    "market": market
                })
            return {"success": True, "data": result, "error": None, "source": "东方财富 push2 API (第一层)"}
        else:
            return {"success": False, "data": None, "error": "未获取到数据", "source": None}
            
    except Exception as e:
        return {"success": False, "data": None, "error": str(e), "source": None}


def get_a_stocks():
    """获取A股自选股行情"""
    return get_realtime_quotes(A_STOCKS)


def get_hk_stocks():
    """获取港股自选股行情"""
    return get_realtime_quotes(HK_STOCKS)


def get_all_stocks():
    """获取全部自选股行情"""
    return get_realtime_quotes(ALL_STOCKS)


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
    import sys
    
    print("=" * 50)
    print("测试A股实时行情")
    print("=" * 50)
    result = get_a_stocks()
    if result["success"]:
        for stock in result["data"]:
            print(f"{stock['name']:10s} {stock['code']:6s} {stock['price']:8.2f} {stock['change_pct']:+6.2f}%")
    else:
        print(f"错误: {result['error']}")
    
    print("\n" + "=" * 50)
    print("测试港股实时行情")
    print("=" * 50)
    result = get_hk_stocks()
    if result["success"]:
        for stock in result["data"]:
            print(f"{stock['name']:10s} {stock['code']:6s} {stock['price']:8.2f} {stock['change_pct']:+6.2f}%")
    else:
        print(f"错误: {result['error']}")
