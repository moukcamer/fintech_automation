
from finance.models import Transaction
from ai.services import compute_transaction_ai
from accounting.services import post_transaction


def create_transaction(**data):

    transaction = Transaction.objects.create(**data)

    # AI
    ai_result = compute_transaction_ai(transaction)

    transaction.fraud_probability = ai_result["fraud_probability"]
    transaction.is_fraud = ai_result["is_fraud"]
    transaction.ai_status = ai_result["status"]
    transaction.save()

    # Accounting
    post_transaction(transaction)

    return transaction
