from django.shortcuts import render
import json
from django.views import View
from .models import Legajo, DatosPersonales
from django.conf import settings


def construir_estructura_organigrama(legajos):
    legajos_dict = []

    for legaj in legajos:
        if legaj.superior_inmediato:
            superior = DatosPersonales.objects.get(legajo=legaj.superior_inmediato.id).apellido + ", " + DatosPersonales.objects.get(legajo=legaj.superior_inmediato.id).nombre
        else: 
            superior = "-"

        legajo = {
            "id": legaj.id,
            "pid": legaj.superior_inmediato_id,
            "superior_inmediato": superior,
            "nombre": DatosPersonales.objects.get(legajo=legaj).apellido + ", " + DatosPersonales.objects.get(legajo=legaj).nombre,
            "nacimiento": str(DatosPersonales.objects.get(legajo=legaj).nacimiento) ,
            "puesto": legaj.cargo.descripcion,
            "sector": legaj.sector.nombre,
            "oficina": legaj.oficina.descripcion,
            "img": DatosPersonales.objects.get(legajo=legaj).foto.name
        }
        print(legajo)
        legajos_dict.append(legajo)

    return legajos_dict

class OrganigramaView(View):
    template_name = 'organigrama_template.html'

    def get_context_data(self, **kwargs):
        legajos = Legajo.objects.all()
        data = construir_estructura_organigrama(legajos)
        data = json.dumps(data)
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'data': data,
        }

        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
