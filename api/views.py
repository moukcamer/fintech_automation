from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .serializers import ContactMessageSerializer

import random


@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Bienvenue sur l'API MoukFinTech"
    })


@api_view(['GET'])
def monthly_performance(request):

    data = [
        {"month": "Jan", "revenue": random.randint(1000, 5000)},
        {"month": "Feb", "revenue": random.randint(1000, 5000)},
        {"month": "Mar", "revenue": random.randint(1000, 5000)},
        {"month": "Apr", "revenue": random.randint(1000, 5000)},
        {"month": "May", "revenue": random.randint(1000, 5000)},
        {"month": "Jun", "revenue": random.randint(1000, 5000)},
    ]

    return Response(data)







