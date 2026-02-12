def build_features(transactions):
    return {
        "avg_amount": transactions.aggregate(Sum("amount"))["amount__sum"],
        "count": transactions.count(),
    }
