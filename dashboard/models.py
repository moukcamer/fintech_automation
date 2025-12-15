from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from finance.models import Invoice


class Customer(models.Model):
    """
    Représente un client enregistré dans la plateforme.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Numéro de téléphone du client"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Adresse complète du client"
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ville de résidence du client"
    )

    country = models.CharField(
        max_length=100,
        default="Cameroun",
        help_text="Pays du client"
    )

    profile_completed = models.BooleanField(
        default=False,
        help_text="Indique si le client a complété son profil"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date de création du compte client"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière mise à jour"
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# dashboard/models.py

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('current', 'Compte courant'),
        ('savings', 'Compte épargne'),
        ('business', 'Compte entreprise'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="accounts"
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    issued_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer} - {self.get_account_type_display()}"



class Transaction(models.Model):
    """
    Historique des transactions d’un compte.
    """
    TRANSACTION_TYPES = (
        ('deposit', 'Dépôt'),
        ('withdrawal', 'Retrait'),
        ('transfer', 'Transfert'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(default=timezone.now)  # remplit automatiquement
    issued_at = models.DateTimeField(default=timezone.now) 


    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class Notification(models.Model):
    """
    Messages envoyés à l’utilisateur suite aux opérations financières.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.customer}"


class DashboardStats(models.Model):
    """
    Statistiques affichées sur le tableau de bord.
    """
    total_customers = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Statistique du dashboard"
        verbose_name_plural = "Statistiques du dashboard"

    def __str__(self):
        return "Statistiques générales"

# dashboard/models.py

# Définissez d'abord vos choix de paiement
PAYMENT_TYPES = [
    ("IN", "Incoming"),   # Paiement entrant
    ("OUT", "Outgoing"),  # Paiement sortant
]

from django.utils import timezone

class Payment(models.Model):
    invoice = models.ForeignKey(
        'dashboard.Invoice',  # ou 'finance.Invoice'
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("CASH", "Cash"),
            ("MOBILE_MONEY", "Mobile Money"),
            ("BANK_TRANSFER", "Bank Transfer")
        ],
        default="CASH"
    )
    payment_type = models.CharField(
        max_length=3,
        choices=[("IN", "Incoming"), ("OUT", "Outgoing")],
        default="IN"
    )
    date = models.DateTimeField(default=timezone.now)  # <-- valeur par défaut dynamique

    def __str__(self):
        return f"Payment {self.amount} for {self.invoice}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    issued_to = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    company_id = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    issued_at = models.DateTimeField(auto_now_add=True)
    documents = models.FileField(upload_to='invoices/', blank=True, null=True)
    payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.issued_to}"

    class Meta:
        ordering = ['-issued_at']
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"


