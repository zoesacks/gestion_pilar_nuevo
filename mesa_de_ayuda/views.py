from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import SolicitudDeAyuda, ComentarioSolicutudDeAyuda
from .serializers import SolicitudDeAyudaSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.exceptions import ValidationError


def obtener_solicitud_o_404(pk):
    queryset = SolicitudDeAyuda.objects.all()
    return get_object_or_404(queryset, pk=pk)

def agregarfoto(solicitud, imagen, usuario):
    nuevo_comentario = ComentarioSolicutudDeAyuda(foto=imagen, usuario=usuario)
    nuevo_comentario.save()
    solicitud.comentarios.add(nuevo_comentario)

def agregarComentario(solicitud, comentario, usuario):
    nuevo_comentario = ComentarioSolicutudDeAyuda(comentario=comentario, usuario=usuario)
    nuevo_comentario.save()
    solicitud.comentarios.add(nuevo_comentario)
    return nuevo_comentario


def mesaDeAyuda(request):
    
    context = {
    }

    return render(request, 'mesaDeAyuda.html', context)




class NuevoComentarioView(APIView):
       def put(self, request, pk):
        solicitud = obtener_solicitud_o_404(pk)
        comentario = request.data.get('comentario', None)
        imagen = request.data.get('foto', None)
        
        if comentario:
            nuevo_comentario = ComentarioSolicutudDeAyuda(comentario=comentario, usuario=request.user)
            nuevo_comentario.save()
            solicitud.comentarios.add(nuevo_comentario)

            response_data = {
            'comentario': nuevo_comentario.comentario,
            'fecha': nuevo_comentario.fecha,
            'usuario': {
                    'id': nuevo_comentario.usuario.id,
                    'username': nuevo_comentario.usuario.username,
                    'email': nuevo_comentario.usuario.email,
                },
            }

            return JsonResponse({'message': 'Comentario agregado exitosamente', 'comentario': response_data}, status=status.HTTP_201_CREATED)

        elif imagen:
            try:
                agregarfoto(solicitud, imagen, request.user)
                return JsonResponse({'message': 'Imagen agregada exitosamente'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return JsonResponse({'message': f'Error al agregar la imagen: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'Hubo un error'}, status=status.HTTP_200_OK)
    

class SolicitudDeAyudaView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk is not None:
            solicitud = get_object_or_404(SolicitudDeAyuda, id=pk, usuario=request.user)
            serializador = SolicitudDeAyudaSerializer(solicitud)
        else:
            instancias = SolicitudDeAyuda.objects.filter(usuario=request.user)
            serializador = SolicitudDeAyudaSerializer(instancias, many=True)
            
        datos_serializados = serializador.data

        return Response(datos_serializados)
    
    def post(self, request):
        datos_solicitud = request.data
        datos_solicitud['usuario'] = request.user.id
        serializador = SolicitudDeAyudaSerializer(data=datos_solicitud)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)