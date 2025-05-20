from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Employer
from .serializers import EmployerSerializer

class EmployerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employers = Employer.objects.filter(user=request.user)
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Employer.objects.get(pk=pk, user=user)
        except Employer.DoesNotExist:
            return None

    def get(self, request, pk):
        employer = self.get_object(pk, request.user)
        if not employer:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = EmployerSerializer(employer)
        return Response(serializer.data)

    def put(self, request, pk):
        employer = self.get_object(pk, request.user)
        if not employer:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = EmployerSerializer(employer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        employer = self.get_object(pk, request.user)
        if not employer:
            return Response({'detail': 'Not found.'}, status=404)
        employer.delete()
        return Response({'detail': 'Deleted'}, status=204)
