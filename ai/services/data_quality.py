import pandas as pd
import numpy as np

class DataQualityService:

    @staticmethod
    def report(df: pd.DataFrame):
        return {
            "missing_values": df.isnull().sum().to_dict(),
            "outliers": DataQualityService.detect_outliers(df)
        }

    @staticmethod
    def detect_outliers(df):
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1

            outliers[col] = int(
                ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum()
            )

        return outliers

    @staticmethod
    def clean(df):
        df = df.fillna(df.median(numeric_only=True))
        return df
