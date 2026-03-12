from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from finance.models import Transaction
from api.serializers import TransactionSerializer


@api_view(["POST"])
def create_transaction(request):

    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        transaction = serializer.save()

        return Response({
            "status": "success",
            "transaction_id": transaction.id
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)