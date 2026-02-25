from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Choisir un fichier CSV ou Excel")