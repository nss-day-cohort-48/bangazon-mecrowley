from django.urls import path
from .views import customer_favorite_sellers_list

urlpatterns = [
    path('reports/favoritesellers', customer_favorite_sellers_list),
]
