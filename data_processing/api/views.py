from django.http import JsonResponse
from finance.models import Payment
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.db import models


def kpis(request):
    income = Payment.objects.filter(payment_type="IN").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    expense = Payment.objects.filter(payment_type="OUT").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return JsonResponse({
        "total_income": income,
        "total_expense": expense,
        "net_result": income - expense
    })


def monthly_performance(request):
    qs = (
        Payment.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=~models.Q(invoice=None)),
            expense=Sum("amount", filter=models.Q(invoice=None)),
        )
        .order_by("month")
    )

    labels = []
    values = []

    for row in qs:
        labels.append(row["month"].strftime("%b %Y"))
        income = row["income"] or 0
        expense = row["expense"] or 0
        values.append(income - expense)

    return JsonResponse({
        "labels": labels,
        "values": values
    })




def top_clients(request):
    qs = (
        Payment.objects
        .filter(invoice__isnull=False)
        .values(
            "invoice__customer_name",
            "invoice__customer_email"
        )
        .annotate(total=Sum("amount"))
        .order_by("-total")[:10]
    )

    data = [
        {
            "customer": row["invoice__customer_name"],
            "email": row["invoice__customer_email"],
            "total": row["total"]
        }
        for row in qs
    ]

    return JsonResponse(data, safe=False)


