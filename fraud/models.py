from django.db import models
from finance.models import Transaction
from accounts.models import User

class Transaction(models.Model):

    STATUS_CHOICES = (
        ("normal", "Normal"),
        ("suspect", "Suspect"),
        ("fraud", "Frauduleux"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fraud_transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=150)
    device = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()

    risk_score = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="normal")

    def __str__(self):
        return f"{self.user.email} - {self.amount} FCFA ({self.status})"



class FraudAlert(models.Model):

    RISK_LEVELS = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="fraud_alerts"
    )

    risk_score = models.FloatField()
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default="low"
    )

    reason = models.TextField(blank=True, null=True)

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fraud Alert - {self.transaction.id} - {self.risk_level}"

