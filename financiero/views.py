from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def flujoFinanciero(request):

    user_name = request.user.username
    puesto = 'Coordinador'

    context = {
        'titulo' : '',
        'user' : user_name,
        'puesto':puesto,
        }

    return render(request, 'financiero.html', context)