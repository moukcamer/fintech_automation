from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.models import Payment


@receiver(post_save, sender=Payment)
def payment_accounting(sender, instance, created, **kwargs):
    if created:
        from accounting.services import record_double_entry
        record_double_entry(instance)



from .models import Transaction
from ml.services import detect_fraud

@receiver(post_save, sender=Transaction)
def check_fraud(sender, instance, created, **kwargs):

    if created:
        instance.is_fraud = detect_fraud(instance)
        instance.save(update_fields=["is_fraud"])
