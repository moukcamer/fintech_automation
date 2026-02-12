import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from finance.models import Transaction


MODEL_PATH = "ml/fraud_model.pkl"


def train_fraud_model():

    transactions = Transaction.objects.all().values(
        "amount", "transaction_type", "country"
    )

    df = pd.DataFrame(list(transactions))

    if df.empty:
        return

    df["transaction_type"] = df["transaction_type"].map({"IN": 1, "OUT": 0})

    model = IsolationForest(contamination=0.02)
    model.fit(df)

    joblib.dump(model, MODEL_PATH)