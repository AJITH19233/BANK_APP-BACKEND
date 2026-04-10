from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Beneficiary
from .serializers import BeneficiarySerializer

class BeneficiaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        beneficiaries = Beneficiary.objects.filter(user=request.user)
        serializer = BeneficiarySerializer(beneficiaries, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = BeneficiarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)