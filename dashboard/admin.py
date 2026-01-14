from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse

from finance.models import Invoice, Payment, Account


def admin_dashboard_view(request):
    """
    Dashboard financier intégré à l'administration Django
    Accessible via /admin/dashboard/
    """
    context = dict(
        admin.site.each_context(request),

        # KPIs
        total_invoices=Invoice.objects.count(),
        total_payments=Payment.objects.count(),
        total_accounts=Account.objects.count(),

        total_invoice_amount=Invoice.objects.aggregate(
            total=admin.models.Sum("amount")
        )["total"] or 0,

        total_payments_amount=Payment.objects.aggregate(
            total=admin.models.Sum("amount")
        )["total"] or 0,
    )

    return TemplateResponse(
        request,
        "dashboard/admin_dashboard.html",
        context
    )


# =====================================================
# 3️⃣ Injection de l’URL dashboard dans l’admin existant
# =====================================================
def get_admin_urls(original_urls):
    def get_urls():
        urls = original_urls()
        custom_urls = [
            path(
                "dashboard/",
                admin.site.admin_view(admin_dashboard_view),
                name="admin-dashboard",
            ),
        ]
        return custom_urls + urls
    return get_urls


admin.site.get_urls = get_admin_urls(admin.site.get_urls)
