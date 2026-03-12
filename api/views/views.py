from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Bienvenue sur l'API MoukFinTech"
    })


@api_view(['POST'])
def contact_api(request):

    return Response({
        "status": "message recu"
    })




