# accounting/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("ASSET", "Actif"),
        ("LIABILITY", "Passif"),
        ("EQUITY", "Capitaux propres"),
        ("INCOME", "Produit"),
        ("EXPENSE", "Charge"),
    ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)  # ✅ FIX CRITIQUE

    def __str__(self):
        return f"{self.code} - {self.name}"



class Journal(models.Model):
    """
    Journal comptable (BANQUE, CAISSE, VENTES, ACHATS…)
    """
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(models.Model):
    """
    Ligne d'écriture comptable (partie double)
    """
    journal = models.ForeignKey(
        Journal,
        on_delete=models.PROTECT,
        related_name="entries"
    )

    date = models.DateField()
    description = models.CharField(max_length=255)

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="journal_entries"
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00")
    )

    reference = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self):
        return f"{self.date} | {self.account.code} | D:{self.debit} C:{self.credit}"

    def clean(self):
        """
        Règles comptables de base
        """
        if self.debit > 0 and self.credit > 0:
            raise ValueError("Une ligne ne peut pas avoir débit ET crédit")

        if self.debit == 0 and self.credit == 0:
            raise ValueError("Une ligne doit avoir un débit ou un crédit")







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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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




class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ("IN", "Entrée"),
        ("OUT", "Sortie"),
    )

    payment_type = models.CharField(max_length=3, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def post_to_accounting(self):
        if self.payment_type_CHOICES == "IN":
            AccountingService.post_entry(
                reference=f"PAY-{self.id}",
                description="Encaissement client",
                debit_account_code="512",
                credit_account_code="701",
                amount=self.amount
            )
        else:
            AccountingService.post_entry(
                reference=f"PAY-{self.id}",
                description="Paiement fournisseur",
                debit_account_code="601",
                credit_account_code="512",
                amount=self.amount
            )

class Meta:
    permissions = [
        ("view_accounting", "Peut consulter la comptabilité"),
        ("post_entries", "Peut enregistrer des écritures"),
        ("audit_accounting", "Peut auditer la comptabilité"),
    ]





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
