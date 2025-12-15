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
    customer_id = models.ForeignKey('finance.Customer', on_delete=models.CASCADE, null=True, blank=True)


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
    created_at = models.DateTimeField(auto_now_add=True)
    

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
    PAYMENT_TYPES = [
        ("IN", "Incoming"),
        ("OUT", "Outgoing"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    payment_method = models.CharField(max_length=50)

    payment_types = models.CharField(
        max_length=5,
        choices=PAYMENT_TYPES,
        default="IN"
    )


    def __str__(self):
        return f"Payment {self.amount} for {self.invoice}"



class Document(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="finance_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.invoice.invoice_number}"



from django.conf import settings

class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer',        # ← Change ici : nom unique et clair
        verbose_name="Utilisateur associé"
    )
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.phone or self.user.username

    class Meta:
        app_label = 'finance'          # Très important pour que Django reconnaisse finance.Customer
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.phone}"


from django.db import models

class Notification(models.Model):
    customer = models.ForeignKey(
        'finance.Customer',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.customer} - {'Lu' if self.is_read else 'Non lu'}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"



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
