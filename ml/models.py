#ml/models.py

from django.db import models
from django.conf import settings


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="ml/datasets/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MLModel(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version}"


class Prediction(models.Model):
    input_data = models.JSONField()
    prediction = models.JSONField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)



