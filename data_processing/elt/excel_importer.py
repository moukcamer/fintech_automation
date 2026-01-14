import pandas as pd
from .validators import validate_payment_row
from .transform import transform_payment
from .load import load_payments


def import_excel_payments(file):
    """
    Import des paiements depuis un fichier Excel
    Colonnes attendues :
    amount | type | date | description
    """
    df = pd.read_excel(file)

    rows = []
    for _, row in df.iterrows():
        data = row.to_dict()
        validate_payment_row(data)
        rows.append(transform_payment(data))

    load_payments(rows)
    return len(rows)
