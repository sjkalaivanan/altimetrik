from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers
import datetime

# Create your views here.


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages':self.page.paginator.num_pages,
            'results': data
        })


class ProductView(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = StandardPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        name = self.request.query_params.get('product_name', None)
        manufacturer = self.request.query_params.get('manufacturer', None)
        category = self.request.query_params.get('category', None)

        queryset = Product.objects.all()

        if search:
            queryset = queryset.filter(Q(product_name__icontains=search) | Q(manufacturer__icontains=search) |
                                       Q(category__icontains=search))
        if name:
            queryset = queryset.filter(product_name__icontains=name)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
        if category:
            queryset = queryset.filter(category__icontains=category)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_at=datetime.datetime.now(), modified_at=datetime.datetime.now())
