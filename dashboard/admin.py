from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from finance.models import Invoice, Payment, Account

class DashboardAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = dict(
            self.each_context(request),
            total_invoices=Invoice.objects.count(),
            total_payments=Payment.objects.count(),
            total_accounts=Account.objects.count(),
        )
        return TemplateResponse(request, "dashboard/admin_dashboard.html", context)


# instance du nouveau dashboard admin
dashboard_admin = DashboardAdminSite(name="dashboard_admin")
