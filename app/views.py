from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime


def logout(request):
    
    context = {
        'message' : "Hasta Pronto!",
    
        }

    return render(request, 'logout.html', context)

@login_required(login_url='/admin/login/')
def home(request):
    

    # Obtener el nombre del usuario
    user_name = request.user.username
    puesto = "Coordinador"
# ------ fin PROYECCIONES -------------------------------------------------------------------------------

    context = {
        'user' : user_name,
        'puesto':puesto,
        'titulo' : '',
        'mes_actual' : "fecha_actual",
    
        }

    return render(request, 'home.html', context)