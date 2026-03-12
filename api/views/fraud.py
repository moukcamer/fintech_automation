from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from finance.models import Transaction


@api_view(["GET"])
def fraud_check(request, transaction_id):

    try:
        transaction = Transaction.objects.get(id=transaction_id)

    except Transaction.DoesNotExist:
        return Response({
            "error": "Transaction not found"
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({

        "transaction_id": transaction.id,
        "amount": transaction.amount,

        "fraud_probability": transaction.fraud_probability,
        "is_fraud": transaction.is_fraud

    })