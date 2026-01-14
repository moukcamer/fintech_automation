import pandas as pd
from finance.models import Payment

def build_dataset():
    qs = Payment.objects.values(
        "created_at", "amount", "payment_type"
    )
    return pd.DataFrame(qs)
