from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("CONTRACT", "Contract"),
        ("RECEIPT", "Receipt"),
        ("INVOICE", "Invoice"),
        ("REPORT", "Report"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(max_length=100)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    uploaded_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    related_name="uploaded_documents"
)

    file = models.FileField(upload_to="documents/")
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Receipt(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    received_from = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"Receipt for {self.amount}"
