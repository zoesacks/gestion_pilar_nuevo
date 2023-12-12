
from django.contrib import admin
from django.urls import path,include
from app.views import home,logout
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout, name='logout'),
    path('financiero/', include('financiero.urls')),
    path('asientos/', include('asientos.urls')),
    path('seguimiento-expedientes/', include('seguimiento_expedientes.urls')),
    path('mesa-de-ayuda/', include('mesa_de_ayuda.urls')),
    path('recursos_humanos/', include('recursos_humanos.urls')),
    path('', home ,name='home'),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)