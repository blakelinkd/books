from django.urls import path
from .views import ProductDetail, ProductList

app_name = 'products'

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]
