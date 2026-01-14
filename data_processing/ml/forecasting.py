import pandas as pd
from finance.models import Payment


def build_cashflow_dataset():
    qs = Payment.objects.values("created_at", "amount", "payment_type")
    return pd.DataFrame(qs)


def predict_cashflow():
    df = build_cashflow_dataset()
    # modèle ML à brancher ici
    return df.groupby(df["created_at"].dt.month)["amount"].sum()
