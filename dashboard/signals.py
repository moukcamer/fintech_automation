from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def payment_to_accounting(sender, instance, created, **kwargs):
    if created:
        instance.post_to_accounting()
