from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    customer_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    country    = models.CharField(max_length=50)
    city       = models.CharField(max_length=50)
    zip_code   = models.CharField(max_length=20)
    birth_date = models.DateField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.customer_number} - {self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]


class Account(models.Model):
    account_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True
    )

    customer = models.ForeignKey(
        Customer,
        to_field="customer_number",
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    account_type = models.CharField(max_length=30)
    currency     = models.CharField(max_length=10)
    balance      = models.DecimalField(max_digits=15, decimal_places=2)
    open_date    = models.DateField()
    status       = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} ({self.currency})"

    class Meta:
        ordering = ["account_number"]



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("IN", "Crédit"),
        ("OUT", "Débit"),
    )

    transaction_ref = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    account = models.ForeignKey(
        Account,
        to_field="account_number",
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_date = models.DateTimeField()
    amount           = models.DecimalField(max_digits=15, decimal_places=2)
    currency         = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    description      = models.TextField(blank=True)
    channel          = models.CharField(max_length=30)
    country          = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sign = "+" if self.transaction_type == "IN" else "-"
        return f"{self.transaction_ref} {sign}{self.amount}"

    class Meta:
        ordering = ["-transaction_date"]
        indexes = [
            models.Index(fields=["transaction_date"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["account"]),
        ]


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


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ("IN", "Income"),
        ("OUT", "Expense"),
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.payment_type} - {self.amount}"


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
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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


