from django.urls import path, include
from .views import ProductView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product', ProductView, basename='products')

urlpatterns = [
    path('', include(router.urls))
]
