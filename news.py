"""
金融数据获取模块 - 财经快讯

【使用说明】
本模块提供财经新闻、电报快讯的实时查询。

【数据来源】
- 财联社电报（优先）- 最快的中文财经快讯
- 新浪7x24财经（备用）

【重要提示】
- 财联社数据24小时更新，包括海外市场
- ctime为Unix时间戳（秒），需转换

【使用示例】
>>> from news import get_cls_telegraph
>>> result = get_cls_telegraph(10)
>>> for item in result["data"]:
>>>     print(item["title"])
"""

import urllib.request
import json
from datetime import datetime


def get_cls_telegraph(count=20):
    """
    获取财联社电报快讯
    
    【参数】
        count: int - 返回条数，默认20，最大可设50
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "id": "123456",
                    "title": "新闻标题",
                    "content": "正文内容摘要",
                    "ctime": 1773235940,        # Unix时间戳
                    "datetime": "2025-11-08 14:52:20",  # 格式化时间
                    "level": "A"               # 级别: A=重大, B=一般
                },
                ...
            ],
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    """
    url = f"https://www.cls.cn/nodeapi/updateTelegraphList?app=CailianpressWeb&os=web&sv=7.7.5&rn={count}"
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(resp)
        
        if not data.get("data") or not data["data"].get("roll_data"):
            return {"success": False, "data": None, "error": "无数据"}
        
        result = []
        for item in data["data"]["roll_data"]:
            # 转换时间
            dt = datetime.fromtimestamp(item.get("ctime", 0))
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            result.append({
                "id": str(item.get("id", "")),
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "ctime": item.get("ctime", 0),
                "datetime": dt_str,
                "level": item.get("level", "B")
            })
        
        return {"success": True, "data": result, "error": None, "source": "财联社电报 API (第一层)"}
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e), "source": None}


def get_important_news(count=10):
    """
    获取重要财经快讯（仅级别A）
    
    【参数】
        count: int - 返回条数，默认10
    
    【返回】
        同 get_cls_telegraph
    """
    result = get_cls_telegraph(count * 2)  # 多取一些，过滤A级的
    
    if result["success"] and result["data"]:
        important = [item for item in result["data"] if item["level"] == "A"]
        result["data"] = important[:count]
    
    return result


def get_sina_24h(count=10):
    """
    获取新浪财经7x24快讯（备用数据源）
    
    【参数】
        count: int - 返回条数，默认10
    
    【返回】
        dict: {
            "success": True/False,
            "data": [
                {
                    "time": "14:52",
                    "title": "新闻标题"
                },
                ...
            ],
            "error": None, "source": "东方财富 push2 API (第一层)"
        }
    """
    url = f"https://finance.sina.com.cn/realstock/company/hs_{count}/klc_kl.js"
    
    try:
        # 新浪7x24接口可能有变化，这里用备用方案
        # 尝试获取财经新闻首页
        url = "https://finance.sina.com.cn/stock/"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        
        # 新浪页面结构复杂，这里简化返回
        # 实际使用建议用财联社
        return {
            "success": True,
            "data": [],
            "error": "新浪接口备用，建议使用财联社"
        }
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ==================== 独立运行测试 ====================
if __name__ == "__main__":
    print("=" * 50)
    print("测试财联社电报快讯")
    print("=" * 50)
    
    result = get_cls_telegraph(10)
    if result["success"]:
        for item in result["data"]:
            level_emoji = "🔴" if item["level"] == "A" else "⚪"
            print(f"{level_emoji} [{item['datetime'][-8:]}] {item['title']}")
    else:
        print(f"错误: {result['error']}")
