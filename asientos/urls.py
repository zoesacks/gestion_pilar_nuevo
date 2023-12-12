# financiero/urls.py
from django.urls import path
from asientos.views import gastos,ingresos,prestamos

urlpatterns = [
    path('gastos/', gastos, name='gastos'),
    path('ingresos/', ingresos, name='ingresos'),
    path('prestamos/', prestamos, name='prestamos'),
]
