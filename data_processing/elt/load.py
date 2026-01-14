from finance.models import Payment

def load_payments(rows):
    for row in rows:
        Payment.objects.create(**row)
