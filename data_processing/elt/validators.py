class ValidationError(Exception):
    pass


REQUIRED_FIELDS = ["amount", "type", "date"]


def validate_payment_row(row: dict):
    for field in REQUIRED_FIELDS:
        if field not in row or row[field] in (None, ""):
            raise ValidationError(f"Champ requis manquant : {field}")

    if row["type"] not in ("credit", "debit"):
        raise ValidationError("Type invalide (credit/debit)")

    try:
        float(row["amount"])
    except ValueError:
        raise ValidationError("Montant invalide")
