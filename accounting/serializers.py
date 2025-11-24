# accounting/serializers.py
from rest_framework import serializers
from .models import Invoice, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'supplier', 'invoice_number', 'date_issued', 'amount', 'vat', 'status', 'raw_file', 'ocr_status', 'ocr_data', 'extracted_data']
        read_only_fields = ['ocr_status', 'ocr_data', 'extracted_data']
