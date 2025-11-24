from django.contrib import admin
from .models import Company, Profile, AuditLog

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(AuditLog)
