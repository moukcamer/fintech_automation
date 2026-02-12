from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from .services import calculate_risk, classify

@receiver(post_save, sender=Transaction)
def detect_fraud(sender, instance, created, **kwargs):
    if created:
        score = calculate_risk(instance)
        status = classify(score)

        instance.risk_score = score
        instance.status = status
        instance.save(update_fields=["risk_score", "status"])
