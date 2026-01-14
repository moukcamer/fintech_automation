from django.contrib import admin
from .models import Account, Transaction, Invoice, Payment, Journal, Entry, EntryLine, JournalEntry

admin.site.register(Transaction)
admin.site.register(Invoice)
admin.site.register(Payment)



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "account_type")
    list_filter = ("account_type",)
    search_fields = ("code", "name")


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "journal", "account", "debit", "credit", "reference",)
    list_filter = ("journal", "account","date",)
    search_fields = ("description", "reference", "account__code", "account___name",)
    date_hierarchy = "date"
    
class EntryLineInline(admin.TabularInline):
    model = EntryLine
    extra = 2


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("reference", "journal", "date", "total_debit", "total_credit")
    inlines = [EntryLineInline]
