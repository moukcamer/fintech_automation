from django.test import TestCase
from django.contrib.auth import get_user_model
from finance.models import Account, Transaction
from accounting.models import Payment, JournalEntry
from fraud.services import check_fraud
from ai.services import compute_transaction_ai

User = get_user_model()


class FinanceTestCase(TestCase):

    def test_account_creation(self):
        account = Account.objects.create(
            name="Client A",
            account_number="1001",
            balance=1000
        )

        self.assertEqual(account.balance, 1000)
        self.assertEqual(account.account_number, "1001")


class FullFintechFlowTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="flow@test.com",
            password="1234"
        )

    def test_full_transaction_flow(self):

        # 1️⃣ Create account
        debit_account = Account.objects.create(
            name="Debit Account",
            account_number="2001",
            balance=0
        )

        credit_account = Account.objects.create(
            name="Credit Account",
            account_number="2002",
            balance=0
        )

        # 2️⃣ Create transaction
        transaction = Transaction.objects.create(
            account=debit_account,
            amount=1500000,
            status="PENDING"
        )

        # 3️⃣ AI scoring
        ai_result = compute_transaction_ai(transaction)
        self.assertIn("risk_score", ai_result)
        self.assertIn("fraud_probability", ai_result)
        self.assertIn("is_fraud", ai_result)

        # 4️⃣ Fraud check
        fraud_result = check_fraud(amount=transaction.amount)
        self.assertIn("risk_score", fraud_result)
        self.assertTrue(fraud_result["risk_score"] >= 0)

        # 5️⃣ Create payment
        payment = Payment.objects.create(
            debit_account=debit_account,
            credit_account=credit_account,
            amount=transaction.amount,
            status="COMPLETED"
        )

        if hasattr(payment, "post"):
            payment.post()
        

        # 6️⃣ Assertions
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.amount, transaction.amount)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(JournalEntry.objects.count(), 1)







