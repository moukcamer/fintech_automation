from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from finance.models import Transaction


# 1️⃣ Performance mensuelle (déjà dans votre projet)
@api_view(["GET"])
def monthly_performance(request):

    data = (
        Transaction.objects
        .annotate(month=TruncMonth("posted_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    labels = []
    values = []

    for item in data:
        labels.append(item["month"].strftime("%b %Y"))
        values.append(float(item["total"] or 0))

    return Response({
        "labels": labels,
        "values": values
    })


# 2️⃣ Résumé financier global (nouvelle API)
@api_view(["GET"])
def financial_summary(request):

    total_transactions = Transaction.objects.count()

    fraud_transactions = Transaction.objects.filter(
        is_fraud=True
    ).count()

    total_volume = Transaction.objects.aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return Response({

        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "total_volume": total_volume

    })