from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.data_quality import DataQualityService

@api_view(["GET"])
def ai_health_check(request):
    return Response({
        "status": "AI online",
        "modules": [
            "data_quality",
            "anomaly_detection",
            "forecasting"
        ]
    })
