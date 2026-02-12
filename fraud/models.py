

from django.db import models
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