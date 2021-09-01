from django.urls import path
from .views import customer_favorite_sellers_list
from .views import incomplete_orders_list

urlpatterns = [
    path('reports/favoritesellers', customer_favorite_sellers_list),
    path('reports/incompleteorders', incomplete_orders_list),
]
