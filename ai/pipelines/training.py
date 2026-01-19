import pandas as pd

from ai.services.data_quality import DataQualityService
from ai.services.anomaly_detection import AnomalyDetectionService
from ai.services.forecasting import FinancialForecastService


class TrainingPipeline:
    """
    Pipeline d'entraînement IA
    """

    def __init__(self):
        self.anomaly_model = AnomalyDetectionService()
        self.forecast_model = FinancialForecastService()

    def run(self, df: pd.DataFrame):
        # 1️⃣ Nettoyage données
        df = DataQualityService.clean(df)

        # 2️⃣ Entraînement détection anomalies
        features = df.select_dtypes(include="number")
        self.anomaly_model.fit(features)

        # 3️⃣ Entraînement modèle de prévision
        if "target" in df.columns:
            self.forecast_model.train(df.drop(columns=["target"]), target="target")

        return {
            "status": "training_completed",
            "rows": len(df),
            "features_used": list(features.columns),
        }
