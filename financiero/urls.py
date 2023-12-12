# financiero/urls.py
from django.urls import path
from financiero.views import flujoFinanciero

urlpatterns = [
    path('flujo-financiero/', flujoFinanciero, name='flujo-financiero'),
]
