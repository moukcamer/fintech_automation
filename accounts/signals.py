# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import User, UserProfile, FinancialPermission, LoginHistory


# ======================================================
# CREATION AUTOMATIQUE PROFIL + PERMISSIONS
# ======================================================
@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:

        # 1️⃣ Profil utilisateur
        UserProfile.objects.create(
            user=instance,
            timezone="Africa/Douala",
            language="fr",
            receive_notifications=True
        )

        # 2️⃣ Permissions financières par défaut
        # (adaptées selon rôle)
        if instance.role == "ADMIN":
            FinancialPermission.objects.create(
                user=instance,
                can_view_financial_data=True,
                can_validate_transactions=True,
                can_export_reports=True,
                can_manage_users=True,
                daily_limit=None  # illimité
            )

        elif instance.role == "ACCOUNTANT":
            FinancialPermission.objects.create(
                user=instance,
                can_view_financial_data=True,
                can_validate_transactions=True,
                can_export_reports=True,
                can_manage_users=False,
                daily_limit=50000000
            )

        elif instance.role == "AUDITOR":
            FinancialPermission.objects.create(
                user=instance,
                can_view_financial_data=True,
                can_validate_transactions=False,
                can_export_reports=True,
                can_manage_users=False,
                daily_limit=None
            )

        else:  # STAFF / USER
            FinancialPermission.objects.create(
                user=instance,
                can_view_financial_data=False,
                can_validate_transactions=False,
                can_export_reports=False,
                can_manage_users=False,
                daily_limit=1000000
            )


# ======================================================
# LOG SECURITE A LA PREMIERE CONNEXION
# ======================================================
@receiver(post_save, sender=User)
def create_security_log(sender, instance, created, **kwargs):
    if created:
        LoginHistory.objects.create(
            user=instance,
            ip_address="0.0.0.0",
            user_agent="Account Created",
            successful=True,
            login_time=timezone.now()
        )



# accounts/apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals