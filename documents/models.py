#documents/models.py

from django.db import models
from django.conf import settings



class Document(models.Model):
    DOCUMENT_TYPES = (
        ("invoice", "Facture"),
        ("receipt", "Reçu"),
        ("contract", "Contrat"),
        ("other", "Autre"),
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="documents_uploaded")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Receipt(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    received_from = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"Receipt for {self.amount}"
