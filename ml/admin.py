from django.contrib import admin
from .models import Dataset, MLModel, Prediction

admin.site.register(Dataset)
admin.site.register(MLModel)
admin.site.register(Prediction)
