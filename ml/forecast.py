import numpy as np


def financial_forecast(data, periods=3):

    if len(data) < 2:
        return []

    trend = (data[-1] - data[0]) / len(data)

    forecast = []

    last_value = data[-1]

    for i in range(periods):

        next_value = last_value + trend

        forecast.append(round(next_value, 2))

        last_value = next_value

    return forecast

