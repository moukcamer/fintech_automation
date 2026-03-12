import pandas as pd

def financial_forecast(monthly_data, periods=3):
    """
    Prévision financière simple basée sur la tendance
    """

    if len(monthly_data) < 2:
        return []

    series = pd.Series(monthly_data)

    # calcul tendance
    trend = series.diff().mean()

    last_value = series.iloc[-1]

    forecast = []

    for i in range(periods):
        next_value = last_value + trend
        forecast.append(round(next_value, 2))
        last_value = next_value

    return forecast



