
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

User = get_user_model()


class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"


class Payment(models.Model):

    PAYMENT_TYPE_CHOICES = (
        ("IN", "Income"),
        ("OUT", "Expense"),
    )

    invoice = models.ForeignKey(
        "finance.Invoice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    account = models.ForeignKey(
        "finance.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.payment_type} - {self.amount}"




class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name




class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):


    date = models.DateField(default=timezone.now)

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    transaction_type = models.CharField( max_length=50 )

    status = models.CharField(max_length=30)

    description = models.TextField(blank=True)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"



class Document(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="finance_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.invoice.invoice_number}"



class DashboardStats(models.Model):
    total_customers = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats au {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Statistique du Dashboard"
        verbose_name_plural = "Statistiques du Dashboard"
        ordering = ['-updated_at']



def prevent_if_closed():	
    now = timezone.now()
    if AccountingPeriod.objects.filter(
        month=now.month,
        year=now.year,
        is_closed=True
    ).exists():
        raise ValidationError("Période comptable clôturée")


