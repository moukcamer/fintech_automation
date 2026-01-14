import csv
from finance.models import Payment


def import_payments_csv(file):
    reader = csv.DictReader(file.read().decode("utf-8").splitlines())

    for row in reader:
        Payment.objects.create(
            amount=row.get("amount", 0),
            payment_type=row.get("type", "IN"),
            created_at=row.get("date"),
            description=row.get("description", "")
        )
