from django.db import models
from finance.models import Transaction


class AITransactionScore(models.Model):

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="ai_score"
    )

    risk_score = models.FloatField()
    anomaly_score = models.FloatField(null=True, blank=True)

    model_version = models.CharField(
        max_length=50,
        default="v1.0"
    )

    prediction_label = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Score - Tx {self.transaction.id} - {self.risk_score}"