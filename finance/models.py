# finance/models.py

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid
from datetime import date


def generate_tx_ref():
    return "TX-" + uuid.uuid4().hex[:12].upper()



class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ("IN", "Credit"),
        ("OUT", "Debit"),
    ]

    CHANNELS = [
        ("BANK", "Bank Transfer"),
        ("MOBILE", "Mobile Money"),
        ("CARD", "Card Payment"),
        ("CASH", "Cash"),
        ("OTHER", "Other"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("FLAGGED", "Flagged"),
    ]

    # ========================
    # CORE FIELDS
    # ========================

    transaction_ref = models.CharField(
        max_length=50,
        unique=True,
        default=generate_tx_ref,
        editable=False
    )

    account = models.ForeignKey(
        "finance.Account",
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)

    transaction_type = models.CharField(
        max_length=3,
        choices=TRANSACTION_TYPES,
        default="IN"
    )

    description = models.TextField(blank=True, null=True)

    currency =models.CharField(max_length=10, default="XAF")

    transaction_date = models.DateTimeField(default=timezone.now)

    channel = models.CharField(
        max_length=10,
        choices=CHANNELS,
        default="OTHER"
    )

    country = models.CharField(max_length=50, blank=True, null=True)

    # ========================
    # AI / FRAUD FIELDS
    # ========================

    fraud_probability = models.FloatField(default=0)
    risk_fraud = models.FloatField(default=0)
    is_fraud = models.BooleanField(default=False)
    ai_comment = models.TextField(blank=True, null=True)
    ai_status = models.CharField(max_length=20, default="PENDING")

    # ========================
    # ACCOUNTING FIELDS
    # ========================

    is_posted = models.BooleanField(default=False)
    posted_at = models.DateTimeField(blank=True, null=True)

    # ========================
    # STATUS / META
    # ========================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========================
    # SAVE OVERRIDE (SAFE)
    # ========================

    def save(self, *args, **kwargs):

        # Si transaction postée → on met date
        if self.is_posted and not self.posted_at:
            self.posted_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_ref} - {self.amount} XAF"



class Customer(models.Model):
    customer_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True
    )

    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True,
        db_index=True
    )

    country = models.CharField(max_length=50)
    city    = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    birth_date = models.DateField()

    # ✅ automatique à la création
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ mis à jour à chaque save
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # Business Logic
    # -------------------------

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return f"{self.customer_number} - {self.get_full_name()}"

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["customer_number"]),
            models.Index(fields=["email"]),
        ]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"



class Account(models.Model):

    ACCOUNT_TYPES = [
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("REVENUE", "Revenue"),
        ("EXPENSE", "Expense"),
        ("CUSTOMER", "Customer Account"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("SUSPENDED", "Suspended"),
        ("CLOSED", "Closed"),
    ]

    # =========================
    # IDENTIFICATION
    # =========================

    account_number = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(max_length=100)

    # ✅ RELATION PROFESSIONNELLE
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accounts"
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
    )

    currency = models.CharField(
        max_length=5,
        default="XAF"
    )

    # =========================
    # FINANCIAL
    # =========================

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    credit_score = models.FloatField(default=0)

    # =========================
    # STATUS & META
    # =========================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    open_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.name}"

class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id}"


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="finance_documents")
    file = models.FileField(upload_to="finance_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document invoice #{self.invoice_id}"


class DashboardStats(models.Model):
    total_customers = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

