"""
金融数据获取模块 - 北向资金（沪深港通）

【使用说明】
本模块提供北向资金（沪股通+深股通）的实时流向数据。

【数据说明】
- 北向资金 = 沪股通 + 深股通（外资买入A股）
- 南向资金 = 港股通（内地资金买入港股）

【重要提示】
- 开盘后几分钟内数据可能有"-"，需等待数据聚合
- 盘后（15:00后）数据最完整
- 数据单位：元（需除以10000转为亿）

【使用示例】
>>> from north_money import get_north_money
>>> result = get_north_money()
>>> print(result["data"])
"""

import urllib.request
import json
from datetime import datetime


def get_north_money():
    """
    获取北向资金实时流向
    
    【返回】
        dict: {
            "success": True/False,
            "data": {
                "sh_net": 52.3,        # 沪股通净流入(亿元)
                "sz_net": 35.8,        # 深股通净流入(亿元)
                "total_net": 88.1,     # 北向资金净流入合计(亿元)
                "sh_accum": 520.5,     # 沪股通累计净流入(亿元)
                "sz_accum": 320.8,     # 深股通累计净流入(亿元)
                "total_accum": 841.3,  # 北向资金累计净流入(亿元)
                "time": "10:30",       # 数据时间
                "raw_time": "10:30:00" # 原始时间
            },
            "error": None 或错误信息
        }
    
    【注意】
        - 开盘后几分钟内可能返回"-"
        - 取最新一条有效数据
    """
    url = "https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if not data.get("data"):
            return {"success": False, "data": None, "error": "无数据"}
        
        # 获取北向资金数据 (s2n = 南向北 = 北向资金流入)
        s2n_list = data["data"].get("s2n", [])
        
        if not s2n_list:
            return {"success": False, "data": None, "error": "无北向资金数据"}
        
        # 找到最后一条有效数据（不是"-"）
        last_valid = None
        for item in reversed(s2n_list):
            if len(item) >= 6 and item[2] != "-" and item[3] != "-":
                last_valid = item
                break
        
        if last_valid is None:
            return {
                "success": True, 
                "data": None, 
                "error": "盘中数据聚合中，请稍后再试"
            }
        
        # 解析数据
        # 格式: [时间, 沪股通净流入, 深股通净流入, 沪股通累计, 深股通累计, 合计]
        time_str = last_valid[0]
        sh_net = _parse_money(last_valid[2])
        sz_net = _parse_money(last_valid[3])
        sh_accum = _parse_money(last_valid[4]) if len(last_valid) > 4 else 0
        sz_accum = _parse_money(last_valid[5]) if len(last_valid) > 5 else 0
        
        return {
            "success": True,
            "data": {
                "sh_net": sh_net,
                "sz_net": sz_net,
                "total_net": sh_net + sz_net,
                "sh_accum": sh_accum,
                "sz_accum": sz_accum,
                "total_accum": sh_accum + sz_accum,
                "time": time_str,
                "raw_time": time_str
            },
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def get_south_money():
    """
    获取南向资金实时流向（内地资金买入港股）
    
    【返回】
        dict: {
            "success": True/False,
            "data": {
                "hk_net": 35.2,       # 港股通净流入(亿元)
                "hk_accum": 520.8,   # 港股通累计净流入(亿元)
                "time": "10:30"
            },
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    """
    url = "https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if not data.get("data"):
            return {"success": False, "data": None, "error": "无数据"}
        
        # 获取南向资金数据 (n2s = 北向南 = 南向资金流出)
        n2s_list = data["data"].get("n2s", [])
        
        if not n2s_list:
            return {"success": False, "data": None, "error": "无南向资金数据"}
        
        # 找最后有效数据
        last_valid = None
        for item in reversed(n2s_list):
            if len(item) >= 2 and item[1] != "-":
                last_valid = item
                break
        
        if last_valid is None:
            return {"success": True, "data": None, "error": "盘中数据聚合中"}
        
        hk_net = _parse_money(last_valid[1])
        hk_accum = _parse_money(last_valid[3]) if len(last_valid) > 3 else 0
        
        return {
            "success": True,
            "data": {
                "hk_net": hk_net,
                "hk_accum": hk_accum,
                "time": last_valid[0]
            },
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def _parse_money(val):
    """
    解析金额数据
    
    【参数】
        val: str - 原始值，如 "5200000.00" 或 "-"
    
    【返回】
        float - 亿元（已除以10000）
    """
    if val is None or val == "-" or val == "":
        return 0.0
    
    try:
        # 原始单位是元，转为亿
        return float(val) / 100000000
    except:
        return 0.0


# ==================== 独立运行测试 ====================
if __name__ == "__main__":
    print("=" * 50)
    print("测试北向资金（沪股通+深股通）")
    print("=" * 50)
    
    result = get_north_money()
    if result["success"]:
        if result["data"]:
            d = result["data"]
            print(f"时间: {d['time']}")
            print(f"沪股通净流入: {d['sh_net']:+.2f}亿")
            print(f"深股通净流入: {d['sz_net']:+.2f}亿")
            print(f"合计净流入:   {d['total_net']:+.2f}亿")
            print(f"沪股通累计:   {d['sh_accum']:.2f}亿")
            print(f"深股通累计:   {d['sz_accum']:.2f}亿")
            print(f"累计合计:     {d['total_accum']:.2f}亿")
        else:
            print(f"提示: {result['error']}")
    else:
        print(f"错误: {result['error']}")
    
    print("\n" + "=" * 50)
    print("测试南向资金（港股通）")
    print("=" * 50)
    
    result = get_south_money()
    if result["success"]:
        if result["data"]:
            d = result["data"]
            print(f"时间: {d['time']}")
            print(f"港股通净流入: {d['hk_net']:+.2f}亿")
            print(f"累计净流入:   {d['hk_accum']:.2f}亿")
        else:
            print(f"提示: {result['error']}")
    else:
        print(f"错误: {result['error']}")
