from django.urls import path
from .views import mesaDeAyuda


urlpatterns = [
    path('', mesaDeAyuda, name='mesaDeAyuda'),
]

