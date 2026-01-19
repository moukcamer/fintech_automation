import pandas as pd
import numpy as np

from ai.services.data_quality import DataQualityService
from ai.services.anomaly_detection import AnomalyDetectionService
from ai.services.forecasting import FinancialForecastService


def sample_dataframe():
    return pd.DataFrame({
        "month": list(range(1, 13)),
        "revenue": [100, 110, 120, 130, None, 150, 160, 1000, 170, 180, 190, 200],
        "expenses": [80, 85, 90, 95, 100, 105, 110, 120, 115, 118, None, 125],
    })


def test_data_quality_report():
    df = sample_dataframe()
    report = DataQualityService.report(df)

    assert "missing_values" in report
    assert "outliers" in report
    assert report["missing_values"]["revenue"] == 1
    assert report["missing_values"]["expenses"] == 1


def test_data_cleaning():
    df = sample_dataframe()
    clean_df = DataQualityService.clean(df)

    assert clean_df.isnull().sum().sum() == 0


def test_anomaly_detection():
    df = sample_dataframe()
    clean_df = DataQualityService.clean(df)

    detector = AnomalyDetectionService()
    detector.fit(clean_df[["revenue", "expenses"]])

    anomalies = detector.predict(clean_df[["revenue", "expenses"]])

    assert len(anomalies) == len(clean_df)
    assert anomalies.sum() >= 1  # au moins une anomalie détectée


def test_forecasting():
    df = sample_dataframe()
    clean_df = DataQualityService.clean(df)

    model = FinancialForecastService()
    model.train(clean_df[["month", "expenses"]], target="revenue")

    future = pd.DataFrame({
        "month": [13, 14, 15],
        "expenses": [130, 135, 140]
    })

    predictions = model.predict(future)

    assert len(predictions) == 3
