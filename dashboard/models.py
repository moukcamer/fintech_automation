from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Représente un client enregistré dans la plateforme.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Account(models.Model):
    """
    Représente le compte financier d’un client.
    """
    ACCOUNT_TYPES = (
        ('current', 'Compte courant'),
        ('savings', 'Compte épargne'),
        ('business', 'Compte entreprise'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class Notification(models.Model):
    """
    Messages envoyés à l’utilisateur suite aux opérations financières.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
