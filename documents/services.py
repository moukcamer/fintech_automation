from accounting.models import Payment


def generate_receipt(payment_id):

    try:
        payment = Payment.objects.get(id=payment_id)

        return {
            "receipt_number": f"RCPT-{payment.id}",
            "amount": payment.amount,
            "status": "generated"
        }

    except Payment.DoesNotExist:
        return {
            "status": "error",
            "message": "Payment not found"
        }