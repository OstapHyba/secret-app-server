from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Secret
from .serializers import SecretSerializer
from .constants import Constants as C

class SecretCreateAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = SecretSerializer

    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        if not serializer.is_valid():
            response = {'error': C.INVALID_INPUT}
            response.update({'message': serializer.errors})
            return Response(
                response,
                status= status.HTTP_405_METHOD_NOT_ALLOWED
                )
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

class SecretGetAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = SecretSerializer

    def get(self, request, uuid):
        try:
            payload = Secret.getDataByHash(uuid)
            serializer = self.serializer_class(data= payload)
            serializer.is_valid(raise_exception= True)
        except NotFound as e:
            return Response(
                {'error': e.__str__()},
                status= e.status_code
                )
        except Exception as e:
            return Response(
                {'error': e.__str__()},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data, status= status.HTTP_200_OK)
