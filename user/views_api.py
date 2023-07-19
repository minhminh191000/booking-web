from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.services import LoginServices 


def _get_data(data):
        return {'data': data}

class LoginAPIView(APIView):
    def get(self, request, format=None):
         return Response({'message':'welcome to API MIGOR v1'}, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        login_api = LoginServices.login_api(data=request.data)
        if not login_api:
            return Response( _get_data({'token':login_api}), status=status.HTTP_400_BAD_REQUEST)
        return Response( _get_data({'token':login_api}), status=status.HTTP_200_OK)