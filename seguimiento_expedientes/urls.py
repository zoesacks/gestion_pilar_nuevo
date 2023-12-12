from django.urls import path
from .views import expedientes

urlpatterns = [
    path('', expedientes, name='expedientes'),
]