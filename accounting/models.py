# accounting/models.py

from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal
from finance.models import Account
from accounts.models import User
from django.utils import timezone
from django.db import models, transaction


class Payment(models.Model):

    PAYMENT_TYPES = [
        ("TRANSFER", "Transfer"),
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("POSTED", "Posted"),
    ]

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    debit_account = models.ForeignKey(
        "finance.Account",
        on_delete=models.PROTECT,
        related_name="debit_payments"
    )

    credit_account = models.ForeignKey(
        "finance.Account",
        on_delete=models.PROTECT,
        related_name="credit_payments"
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES,
        default="TRANSFER"
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PAY-{self.pk} | {self.amount}"

    # ✅ LA MÉTHODE POST DOIT ÊTRE ICI
    def post(self):

        if self.status == "POSTED":
            raise ValidationError("Payment already posted.")

        from accounting.services.posting_engine import post_transaction

        entry = post_transaction(
            debit_account_number=self.debit_account.account_number,
            credit_account_number=self.credit_account.account_number,
            amount=self.amount,
            description=self.description,
            reference=f"PAY-{self.pk}"
        )

        from django.utils import timezone
        self.status = "POSTED"
        self.posted_at = timezone.now()
        self.save(update_fields=["status", "posted_at"])

        return entry


class JournalEntry(models.Model):
    """
    Représente une écriture comptable (double entrée).
    """

    transaction = models.ForeignKey(
        "finance.Transaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="journal_entries"
    )

    reference = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(blank=True)

    entry_date = models.DateTimeField(
        default=timezone.now
    )

    is_posted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-entry_date"]
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return f"{self.reference}"

    # ==============================
    # SAVE OVERRIDE (sécurisé)
    # ==============================

    def save(self, *args, **kwargs):
        if not self.reference:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.reference = f"JE-{timestamp}"
        super().save(*args, **kwargs)

    # ==============================
    # Méthode utilitaire
    # ==============================

    def is_balanced(self):
        total_debit = sum(line.debit for line in self.lines.all())
        total_credit = sum(line.credit for line in self.lines.all())
        return total_debit == total_credit



class JournalLine(models.Model):
    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    account = models.ForeignKey(
        "finance.Account",
        on_delete=models.PROTECT
    )

    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account} - D:{self.debit} C:{self.credit}"



class LedgerEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.account} {self.date}"



class Journal(models.Model):
    """
    Journal comptable (BANQUE, CAISSE, VENTES, ACHATS…)
    """
    account_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account_number} - {self.name}"


class Entry(models.Model):
    """
    Écriture comptable
    """
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    date = models.DateField()
    reference = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.reference

    @property
    def total_debit(self):
        return sum(line.debit for line in self.lines.all())

    @property
    def total_credit(self):
        return sum(line.credit for line in self.lines.all())

    def clean(self):
        if self.total_debit != self.total_credit:
            raise ValidationError("Écriture non équilibrée (débit ≠ crédit)")


class EntryLine(models.Model):
    """
    Ligne d'écriture (débit/crédit)
    """
    entry = models.ForeignKey(
        Entry,
        related_name="lines",
        on_delete=models.CASCADE
    )
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def clean(self):
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("Une ligne ne peut pas être à la fois débit et crédit")

        if self.debit == 0 and self.credit == 0:
            raise ValidationError("Une ligne doit avoir un débit ou un crédit")

    def __str__(self):
        return f"{self.account} | D:{self.debit} C:{self.credit}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DEBIT", "Debit"),
        ("CREDIT", "Credit"),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE, related_name="accounting_transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.amount}"

class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class AccountingPeriod(models.Model):
    """
    Période comptable
    """
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("month", "year")

    def __str__(self):
        return f"{self.month}/{self.year}"
