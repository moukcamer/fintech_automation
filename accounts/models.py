# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# -------------------------
# MANAGER
# -------------------------

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("L'utilisateur doit avoir un email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser doit avoir is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# -------------------------
# USER MODEL
# -------------------------

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email




# =========================================================
# ENTREPRISE / SOCIETE (Multi-tenant)
# =========================================================
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=150, blank=True, null=True)
    tax_number = models.CharField(max_length=150, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, default="Cameroon")

    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =========================================================
# ROLES UTILISATEURS
# =========================================================
class Role(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", _("Super Admin (Platform)")
    ADMIN = "ADMIN", _("Admin Entreprise")
    MANAGER = "MANAGER", _("Manager Financier")
    ACCOUNTANT = "ACCOUNTANT", _("Comptable")
    AUDITOR = "AUDITOR", _("Auditeur")
    VIEWER = "VIEWER", _("Lecture seule")



# =========================================================
# PROFIL UTILISATEUR (infos avancées)
# =========================================================
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    language = models.CharField(max_length=20, default="fr")
    timezone = models.CharField(max_length=50, default="Africa/Douala")

    receive_notifications = models.BooleanField(default=True)
    receive_security_alerts = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile - {self.user.email}"


# =========================================================
# PERMISSIONS FINANCIERES (fine-grained control)
# =========================================================
class FinancialPermission(models.Model):

   user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
   can_view_reports = models.BooleanField(default=True)
   can_export_data = models.BooleanField(default=False)
   can_validate_transactions = models.BooleanField(default=False)
   can_manage_accounts = models.BooleanField(default=False)
   can_manage_budget = models.BooleanField(default=False)
   can_manage_payroll = models.BooleanField(default=False)

def __str__(self):
        return f"Permissions - {self.user.email}"


# =========================================================
# SESSION DE SECURITE
# =========================================================
class LoginHistory(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
   ip_address = models.GenericIPAddressField()
   user_agent = models.TextField(blank=True, null=True)

   login_time = models.DateTimeField(auto_now_add=True)
   successful = models.BooleanField(default=True)

def __str__(self):
        return f"{self.user.email} - {self.ip_address} - {self.login_time}"

