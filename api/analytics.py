from rest_framework.decorators import api_view
from rest_framework.response import Response

from datetime import datetime
import random


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