from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from charities.serializers import BenefactorSerializer


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        benefactor = BenefactorSerializer(data=request.data)
        if benefactor.is_valid():
            benefactor.save(user=request.user)
            return Response({'message': 'User was registered successfully!'})
        
        return Response({'message': benefactor.errors})
