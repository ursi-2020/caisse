from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from application.djangoapp.models import Clik

def index(request):
    if Clik.objects.all():
        clique = Clik.objects.first()
        clique.delete()
    return HttpResponse("Bienvenue sur l'appli caisse")

def helloworld(request):
    return HttpResponse("Hello,je viens de la caisse")

def test(request):

    helloworld = ''
    time = ''
    string = ''

    if not Clik.objects.all():
        clique = Clik(number=0)
        clique.save()
    else:
        clique = Clik.objects.first()
        clique.number = clique.number + 1
        clique.save()
        time = api.send_request('scheduler', 'clock/time')
        helloworld = api.send_request('gestion-magasin', 'hello')
        string = 'Il est'

    context = {
        'time': time,
        'helloworld': helloworld,
        'string': string,
        'clique': clique
    }

    return render(request, 'index.html', context)