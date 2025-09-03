import json
from tv_interval_utils import normalize_interval

def safe_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def parse_tv_payload(payload: str) -> str:
    try:
        data = json.loads(payload)
        symbol = data.get("symbol", "UNKNOWN")
        interval = data.get("interval", "UNKNOWN")
        event = data.get("event", "")
        value = safe_float(data.get("value"))
        raw_desc = data.get("desc", "")
        
        # 特殊处理超买/超卖
        if event == "obos_parse_needed":
            if value is None:
                desc = "⚠️ 指标异常"
            elif value >= 40:
                desc = "🔴 超买"
            elif value <= -40:
                desc = "🟢 超卖"
            else:
                desc = "🟡 中性波动"
            desc = desc + raw_desc
        else:
            desc = raw_desc or "⚠️ 无描述"

        msg = f"{symbol} | {normalize_interval(interval)} {desc}"
        if value is not None:
            msg += f"\n指标值: {value:.1f}"

        return msg

    except Exception as e:
        return f"⚠️ JSON解析失败: {e}"
