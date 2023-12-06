from django.urls import path
from .views import show_databases, show_tables

urlpatterns = [
    path('show/', show_databases, name='show_databases'),
    path('tables/', show_tables, name='show_tables'),
]
