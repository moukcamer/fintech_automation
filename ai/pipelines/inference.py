import pandas as pd

from ai.services.data_quality import DataQualityService
from ai.services.anomaly_detection import AnomalyDetectionService
from ai.services.forecasting import FinancialForecastService


class InferencePipeline:
    """
    Pipeline d'inférence IA (temps réel / dashboard)
    """

    def __init__(self, anomaly_model=None, forecast_model=None):
        self.anomaly_model = anomaly_model or AnomalyDetectionService()
        self.forecast_model = forecast_model or FinancialForecastService()

    def run(self, df: pd.DataFrame):
        # 1️⃣ Nettoyage
        df = DataQualityService.clean(df)

        numeric_df = df.select_dtypes(include="number")

        # 2️⃣ Détection anomalies
        anomalies = self.anomaly_model.predict(numeric_df)

        # 3️⃣ Résultat structuré
        results = df.copy()
        results["is_anomaly"] = anomalies

        return results

    def forecast(self, future_df: pd.DataFrame):
        future_df = DataQualityService.clean(future_df)
        return self.forecast_model.predict(future_df)
