from rest_framework import serializers
from .models import SolicitudDeAyuda, ComentarioSolicutudDeAyuda
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)


class ComentarioSolicutudSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(required=False, allow_null=True)
    class Meta:
        model =  ComentarioSolicutudDeAyuda
        fields = '__all__' 
    


class SolicitudDeAyudaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSolicutudSerializer(many=True, required=False)
    desarrollador = UserSerializer(required=False, allow_null=True)

    class Meta: 
        model = SolicitudDeAyuda
        fields = '__all__' 

