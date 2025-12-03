from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,          # ← pour éviter les erreurs makemigrations
        blank=True
    )
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"{self.name} - {self.account_type}"



class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=[("DEBIT", "Debit"), ("CREDIT", "Credit")]
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    issued_to = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("PAID", "Paid"), ("UNPAID", "Unpaid"), ("PARTIAL", "Partial")],
        default="UNPAID"
    )
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("CASH", "Cash"),
            ("MOBILE_MONEY", "Mobile Money"),
            ("BANK_TRANSFER", "Bank Transfer")
        ]
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount} for {self.invoice}"



class Document(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="finance_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.invoice.invoice_number}"
