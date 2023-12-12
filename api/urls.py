from django.urls import path, include, re_path
from mesa_de_ayuda.views import SolicitudDeAyudaView,NuevoComentarioView

from seguimiento_expedientes.views import expedientes, TransferenciaView
from seguimiento_expedientes.api import DocumentoViewSet, UsuarioLogueadoViewSet, UsuariosViewSet

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Mesa de ayuda API",
      default_version='v1',
      description="Descripción de tu API",
      terms_of_service="https://www.tuapi.com/terms/",
      contact=openapi.Contact(email="contact@tuapi.com"),
      license=openapi.License(name="Tu Licencia"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

router.register('documentos', DocumentoViewSet, 'documentos')
router.register('usuarioLogueado', UsuarioLogueadoViewSet, 'usuarioLogueado')
router.register('usuarios', UsuariosViewSet, 'usuarios')

urlpatterns = [
    
    path('solicitud-mesa-ayuda/', SolicitudDeAyudaView.as_view(), name='solicitudDeAyuda'),
    path('solicitud-mesa-ayuda/<int:pk>/', SolicitudDeAyudaView.as_view(), name='solicitud-detalle'),
    path('solicitud-mesa-ayuda/<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),


    path('seguimiento-de-expedientes/transferencia/', TransferenciaView.as_view(), name='generarTransferencia'),
    path('seguimiento-de-expedientes/', include(router.urls)),  


    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
