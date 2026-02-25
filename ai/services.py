def compute_transaction_ai(transaction):

    try:
        score = 0

        if transaction.amount > 1000000:
            score = 90
        elif transaction.amount > 500000:
            score = 65
        else:
            score = 20

        return {
            "risk_score": score,
            "fraud_probability": score / 100,
            "is_fraud": score >= 80,
            "status": "OK"
        }

    except Exception:
        return {
            "risk_score": 0,
            "fraud_probability": 0,
            "is_fraud": False,
            "status": "ERROR"
        }
