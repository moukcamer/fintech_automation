# core/models.py

from django.db import models
from django.conf import settings




class AuditLog(models.Model):
    ACTIONS = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTIONS)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} by {self.user}"

class Organization(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

