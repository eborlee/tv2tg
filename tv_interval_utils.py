# tv_interval_utils.py

def normalize_interval(interval: str) -> str:
    """
    将 TradingView 推送中的 interval 字符串（如 '15', '60', 'D'）转换为标准化格式（如 '15min', '1h', '1d'）

    参数:
        interval (str): TradingView 的 {{interval}} 占位符传入的值

    返回:
        str: 例如 '15min', '1h', '1d'
    """
    interval_map = {
        "1": "1min",
        "3": "3min",
        "5": "5min",
        "15": "15min",
        "30": "30min",
        "60": "1h",
        "120": "2h",
        "240": "4h",
        "D": "1d",
        "W": "1w",
        "M": "1mo",
    }

    # 安全返回
    return interval_map.get(interval, interval)


# 示例用法
if __name__ == "__main__":
    test_cases = ["1", "15", "60", "D", "W", "M", "999"]
    for iv in test_cases:
        print(f"{iv} -> {normalize_interval(iv)}")
