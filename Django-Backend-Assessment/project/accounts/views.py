from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        # TODO: Candidate implementation
        # Validate and save with RegistrationSerializer, then return the success response.
        return Response({"detail": "Registration is not implemented."},
                        status=status.HTTP_501_NOT_IMPLEMENTED)
