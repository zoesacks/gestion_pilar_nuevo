from django import forms
from .widgets import CustomMonthSelectWidget
from .models import ProyeccionGastos, ProyeccionIngresos

class ProyeccionGastosForm(forms.ModelForm):
    class Meta:
        model = ProyeccionGastos
        fields = '__all__'
        widgets = {
            'MES': CustomMonthSelectWidget(),
        }

class ProyeccionIngresosForm(forms.ModelForm):
    class Meta:
        model = ProyeccionIngresos
        fields = '__all__'
        widgets = {
            'MES': CustomMonthSelectWidget(),
        }