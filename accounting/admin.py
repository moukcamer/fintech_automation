from django.contrib import admin
from .models import Account, Transaction, Invoice, Payment, Journal, Entry, EntryLine, JournalEntry, JournalLine

admin.site.register(Transaction)
admin.site.register(Invoice)
admin.site.register(Payment)



@admin.register(JournalLine)
class JournalLineAdmin(admin.ModelAdmin):
    list_display = ("id","journal_entry","account", "debit", "credit", )
    list_filter = ("account",)
    
    
    
class JournalLineInline(admin.TabularInline):
    model = JournalLine
    extra = 0


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction","entry_date", "is_posted")
    list_filter = ( "is_posted", "entry_date")
    
