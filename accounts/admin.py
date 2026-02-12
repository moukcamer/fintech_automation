# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (
    User,
    Company,
    UserProfile,
    FinancialPermission,
    LoginHistory
)
User = get_user_model()

# =========================================================
# INLINE PERMISSIONS FINANCIERES
# =========================================================
class FinancialPermissionInline(admin.StackedInline):
    model = FinancialPermission
    can_delete = False
    extra = 0


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


# =========================================================
# CUSTOM USER ADMIN
# =========================================================
class CustomUserAdmin(UserAdmin):
    model = User

    # ================= DISPLAY =================
    list_display = (
        "email",
        "get_company",
        "get_role",
        "is_active",
        "is_staff",
        "get_verified",
        "last_login",
    )

    list_filter = (
        "is_active",
        "is_staff",
    )

    search_fields = ("email",)
    ordering = ("email",)

    inlines = [UserProfileInline, FinancialPermissionInline]

    # ================= SAFE GETTERS =================
    def get_company(self, obj):
        return getattr(obj, "company", "-")
    get_company.short_description = "Company"

    def get_role(self, obj):
        return getattr(obj, "role", "-")
    get_role.short_description = "Role"

    def get_verified(self, obj):
        return getattr(obj, "is_verified", False)
    get_verified.boolean = True
    get_verified.short_description = "Verified"

    # ================= FIELDSETS =================
    fieldsets = (
        ("Connexion", {"fields": ("email", "password")}),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

# =========================================================
# ENTREPRISE ADMIN
# =========================================================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "phone", "is_active", "created_at")
    search_fields = ("name", "registration_number", "tax_number")
    list_filter = ("country", "is_active")
    ordering = ("name",)


# =========================================================
# HISTORIQUE CONNEXION (SECURITE)
# =========================================================
@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "successful", "login_time")
    list_filter = ("successful", "login_time")
    search_fields = ("user__email", "ip_address")
    readonly_fields = ("user", "ip_address", "user_agent", "login_time")

    def has_add_permission(self, request):
        return False


# =========================================================
# PROFIL (optionnel visible seul)
# =========================================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "timezone", "receive_notifications")
    search_fields = ("user__email",)

