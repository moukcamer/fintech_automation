def safe_decimal(value):
    try:
        return float(value)
    except Exception:
        return 0.0
