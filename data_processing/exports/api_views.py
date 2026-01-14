from django.http import JsonResponse
from finance.models import Payment
from django.db.models import Sum


def kpis_api(request):
    income = Payment.objects.filter(payment_type="IN").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    expense = Payment.objects.filter(payment_type="OUT").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return JsonResponse({
        "income": income,
        "expense": expense,
        "net_result": income - expense
    })
