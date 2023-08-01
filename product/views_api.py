from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from product.services import PorductProduct

def _get_data(data):
        return {'data': data}

class ProductProductView(APIView):

    def get(self, request, format=None):
        # permission_classes = [IsAuthenticated, IsAdminUser]
        return Response(_get_data({'message': 'get Product Done'}), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        permission_classes = [IsAuthenticated, IsAdminUser]
        result = PorductProduct.create_product(products=request.data)
        if result:
            return Response(_get_data({'message': 'Create Product Done'}), status=status.HTTP_201_CREATED)
        return Response(_get_data({'message': 'Create Product Faile'}), status=status.HTTP_400_BAD_REQUEST)