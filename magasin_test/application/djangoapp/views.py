from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    helloworld = api.send_request('caisse', 'helloworld')
    return HttpResponse("L'heure de la clock est %r %r" % (time, helloworld))

def helloworld(request):
    return HttpResponse("Hello, je viens du magasin")