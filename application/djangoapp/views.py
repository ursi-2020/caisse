from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from .models import Article
from datetime import datetime
import json

def index(request):
    return HttpResponse("Bienvenue sur l'appli caisse")

def helloworld(request):
    return HttpResponse("Hello,je viens de la caisse")

def products_update(request):

    if request.method == "POST":
        database_update()

    products = Article.objects.all()

    helloworld = ''
    time = ''
    string = ''


    time = api.send_request('scheduler', 'clock/time')
    helloworld = api.send_request('gestion-magasin', 'hello')
    string = 'Il est'

    context = {
        'time': time,
        'helloworld': helloworld,
        'string': string,
        'products': products
    }

    return render(request, 'index.html', context)

def scheduler(request):

    schedule_result = ""

    if request.method == "POST":
        time = (request.POST.get("time") + ":00").replace('-', '/').replace('T', '-')
        formatted_time = datetime.strptime(time, '%Y/%m/%d-%H:%M:%S')
        formatted_time_str = datetime.strftime(formatted_time, '%d/%m/%Y-%H:%M:%S')
        final_time = datetime.strptime(formatted_time_str, '%d/%m/%Y-%H:%M:%S')
        print(final_time)
        body = {"target_url": "database_update", "target_app": "caisse", "time": final_time, "recurrence": "day", "name": "products_update"}
        print(body)
        schedule_result = api.post_request("scheduler", "schedule/add", body)

    tasks = api.send_request("scheduler", "schedule/list")

    context = {
        'request': schedule_result,
        'tasks': tasks
    }

    return render(request, 'scheduler.html', context)

def database_update():
    Article.objects.all().delete()

    data = api.send_request("catalogue-produit", "catalogueproduit/api/data")

    json_data = json.loads(data)

    for product in json_data["produits"]:
        article = Article(name=product["codeProduit"], price=product["prix"], stock=product["quantiteMin"])
        article.save()
