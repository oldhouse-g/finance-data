"""
金融数据获取模块 - 港股实时行情

【使用说明】
本模块提供港股实时行情查询，数据来源为新浪财经。

【股票代码格式】
- 腾讯控股: 00700
- 阿里巴巴: 09988
- 小米集团: 01810
- 联想集团: 01024

【使用示例】
>>> from hkstocks import get_hk_quote
>>> result = get_hk_quote("00700")
>>> print(result["data"]["price"])
"""

import urllib.request
import json


# 港股代码映射表
HK_CODE_MAP = {
    "00700": "腾讯控股",
    "09988": "阿里巴巴-W",
    "01810": "小米集团-W",
    "01024": "联想集团-W",
    "02318": "中国平安",
    "00981": "中芯国际",
    "03690": "美团-W",
}


def get_hk_quote(code):
    """
    获取单只港股实时行情
    
    【参数】
        code: str - 港股代码，如 "00700"（不需要前缀）
    
    【返回】
        dict: {
            "success": True/False,
            "data": {
                "code": "00700",
                "name": "腾讯控股",
                "price": 546.50,
                "change_pct": -1.00,
                "change_amt": -5.50,
                "prev_close": 552.00,
                "open": 550.00,
                "high": 548.00,
                "low": 545.00,
                "volume": 12345678  # 成交量
            },
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    
    【注意】
        - 返回数据可能有部分字段为空
        - 价格单位：港币
    """
    url = f"https://hq.sinajs.cn/list=rt_hk{code}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("gb2312")
        
        # 解析返回数据
        # 格式: var hq_str_hk00700="腾讯控股,552.00,550.00,548.00,545.00,546.50,-5.50,-1.00,12345678,..."
        if "=" not in resp:
            return {"success": False, "data": None, "error": "数据格式错误", "source": None}
        
        data_str = resp.split("=")[1].strip('"')
        fields = data_str.split(",")
        
        if len(fields) < 10:
            return {"success": False, "data": None, "error": "数据不完整", "source": None}
        
        # 解析字段
        # 0: 名称, 1: 昨收, 2: 今开, 3: 最高, 4: 最低, 5: 最新, 6: 涨跌额, 7: 涨跌幅, 8: 成交量
        name = fields[0]
        prev_close = _safe_float(fields[1])
        open_price = _safe_float(fields[2])
        high = _safe_float(fields[3])
        low = _safe_float(fields[4])
        price = _safe_float(fields[5])
        change_amt = _safe_float(fields[6])
        change_pct = _safe_float(fields[7])
        volume = _safe_int(fields[8])
        
        return {
            "success": True,
            "data": {
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "change_amt": change_amt,
                "prev_close": prev_close,
                "open": open_price,
                "high": high,
                "low": low,
                "volume": volume
            },
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_hk_quotes(codes):
    """
    获取多只港股实时行情
    
    【参数】
        codes: list - 港股代码列表，如 ["00700", "09988"]
    
    【返回】
        dict: {
            "success": True/False,
            "data": [ ... ],  # 同 get_hk_quote 的 data 列表
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    """
    if not codes:
        return {"success": False, "data": None, "error": "代码不能为空", "source": None}
    
    # 拼接请求
    code_list = ",".join([f"rt_hk{c}" for c in codes])
    url = f"https://hq.sinajs.cn/list={code_list}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("gb2312")
        
        results = []
        # 解析每只股票
        for line in resp.split("\n"):
            if "=" not in line:
                continue
            
            code = line.split("=")[0].split("_")[-1]  # 提取代码
            data_str = line.split("=")[1].strip('"')
            fields = data_str.split(",")
            
            if len(fields) < 10:
                continue
            
            results.append({
                "code": code,
                "name": fields[0],
                "price": _safe_float(fields[5]),
                "change_pct": _safe_float(fields[7]),
                "change_amt": _safe_float(fields[6]),
                "prev_close": _safe_float(fields[1]),
                "open": _safe_float(fields[2]),
                "high": _safe_float(fields[3]),
                "low": _safe_float(fields[4]),
                "volume": _safe_int(fields[8])
            })
        
        return {"success": True, "data": results, "error": None, "source": "新浪财经 hq.sinajs.cn (第一层)"}
        
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
    print("测试港股实时行情")
    print("=" * 50)
    
    codes = ["00700", "09988", "01810", "01024"]
    result = get_hk_quotes(codes)
    
    if result["success"]:
        for stock in result["data"]:
            print(f"{stock['name']:12s} {stock['code']:5s} {stock['price']:8.2f} {stock['change_pct']:+6.2f}%")
    else:
        print(f"错误: {result['error']}")
