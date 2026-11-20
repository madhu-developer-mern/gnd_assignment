from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ItemView(APIView):
    http_method_names = ["get", "query", "head", "options"]

    def get(self, request):
        # TODO: Candidate implementation
        # Validate optional pagination, read the items, and serialize the array.
        return Response({"detail": "Item listing is not implemented."},
                        status=status.HTTP_501_NOT_IMPLEMENTED)

    def query(self, request):
        # TODO: Candidate implementation
        # Validate the JSON body, apply the ORM filters, and return total and items.
        return Response({"detail": "Item filtering is not implemented."},
                        status=status.HTTP_501_NOT_IMPLEMENTED)
