from sklearn.ensemble import IsolationForest

class AnomalyDetectionService:

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        preds = self.model.predict(X)
        return preds == -1  # True = anomalie
