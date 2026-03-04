from django.test import TestCase
from finance.models import Account
from accounting.models import Payment, JournalEntry, JournalLine
class AccountingFlowTestCase(TestCase):
    def setUp(self):
        """
        Préparation des données de test.
        """
        self.bank = Account.objects.create(
            account_number="512000",
            name="Banque",
            account_type="ASSET",
            currency="XAF"
        )
        self.client = Account.objects.create(
            account_number="411000",
            name="Client A",
            account_type="ASSET",
            currency="XAF"
        )
    def test_payment_posting_creates_balanced_journal_entry(self):
        """
        Vérifie qu’un paiement crée une écriture équilibrée.
        """
        # Création du paiement
        payment = Payment.objects.create(
            amount=10000,
            debit_account=self.bank,
            credit_account=self.client,
            payment_type="TRANSFER",
            description="Test automated payment"
        )
        # Posting
        entry = payment.post()
        # Vérifie que l’écriture existe
        self.assertIsInstance(entry, JournalEntry)
        # Vérifie qu'il y a 2 lignes
        lines = JournalLine.objects.filter(journal_entry=entry)
        self.assertEqual(lines.count(), 2)
        # Vérifie équilibre débit/crédit
        total_debit = sum(line.debit for line in lines)
        total_credit = sum(line.credit for line in lines)
        self.assertEqual(total_debit, total_credit)
        self.assertEqual(total_debit, 10000)
        # Vérifie que les bons comptes sont utilisés
        debit_line = lines.get(debit=10000)
        credit_line = lines.get(credit=10000)
        self.assertEqual(debit_line.account, self.bank)
        self.assertEqual(credit_line.account, self.client)
        # Vérifie que l’écriture est marquée postée
        entry.refresh_from_db()
        self.assertTrue(entry.is_posted)


class ConcurrentTransactionTestCase(TransactionTestCase):

    reset_sequences = True  # important pour tests concurrence

    def setUp(self):
        self.account = Account.objects.create(
            name="Concurrent Account",
            account_number="7777",
            balance=0
        )

    def process_transaction(self, amount):

        with db_transaction.atomic():

            account = Account.objects.select_for_update.get(id=self.accout.id)

            tx = Transaction.objects.create(
                account=account,
                amount=amount,
                status="PENDING"
            )

            payment = Payment.objects.create(
                debit_account=self.account,
                credit_account=self.account,
                amount=amount,
                status="COMPLETED"
            )

            if hasattr(payment, "post"):
                payment.post()

    def test_concurrent_transactions(self):

        threads = []
        total_threads = 10
        transactions_per_thread = 50

        for _ in range(total_threads):
            t = threading.Thread(
                target=lambda: [
                    self.process_transaction(1000)
                    for _ in range(transactions_per_thread)
                ]
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        expected = total_threads * transactions_per_thread

        self.assertEqual(Transaction.objects.count(), expected)
        self.assertEqual(Payment.objects.count(), expected)
        self.assertEqual(JournalEntry.objects.count(), expected)        