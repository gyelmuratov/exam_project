from django.urls import path

from shop.views import product_list_view, product_detail_view

app_name = 'shop'

urlpatterns = [
    path('', product_list_view, name='list'),
    path('<int:pk>/', product_detail_view, name='detail'),
]
