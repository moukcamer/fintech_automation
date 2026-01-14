import pandas as pd
from finance.models import Payment


def payments_dataset():
    qs = Payment.objects.values(
        "created_at",
        "amount",
        "payment_type",
        "description"
    )
    return pd.DataFrame(qs)
