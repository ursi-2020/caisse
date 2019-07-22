from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def helloworld(request):
    return HttpResponse("Hello,je viens de la caisse")

def test(request):
    time = api.send_request('scheduler','clock/time')
    helloworld = api.send_request('gestion-magasin','hello')


    return HttpResponse("L'heure de la clock est %r. %r"%(time, helloworld))