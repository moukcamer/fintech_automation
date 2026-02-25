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