from django.contrib import admin
from .models import Account, Transaction, Invoice, Payment

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Invoice)
admin.site.register(Payment)
