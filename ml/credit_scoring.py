
from finance.models import Transaction, Account
from django.db.models import Sum


def compute_credit_score(customer):

    accounts = Account.objects.filter(customer=customer)
    balance = accounts.aggregate(Sum("balance"))["balance__sum"] or 0

    transactions = Transaction.objects.filter(account__customer=customer)

    volume = transactions.aggregate(Sum("amount"))["amount__sum"] or 0
    frequency = transactions.count()

    score = 50

    if balance > 1000000:
        score += 20
    if volume > 500000:
        score += 15
    if frequency > 50:
        score += 15

    return min(score, 100)

