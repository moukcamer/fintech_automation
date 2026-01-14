import pandas as pd
from finance.models import Payment


def export_payments_excel():
    qs = Payment.objects.values(
        "created_at", "amount", "payment_type", "description"
    )
    df = pd.DataFrame(qs)

    file_path = "exports/payments_export.xlsx"
    df.to_excel(file_path, index=False)
    return file_path
