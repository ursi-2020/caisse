import requests
from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Article
from datetime import datetime
import json

def index(request):
  #  api.post_request('scheduler', 'app/delete', {"source": "caisse"})
    return HttpResponse("Bienvenue sur l'appli caisse")

def helloworld(request):
    return HttpResponse("Hello,je viens de la caisse")

@csrf_exempt
def products_update(request):

    helloworld = ''
    time = ''
    string = ''
    order_sum = 0
    client = ''
    reduction = 0

    if request.method == "POST":
        if 'order' in request.POST and request.FILES['file']:
            json_data = json.loads(request.FILES['file'].read())
            order_sum = load_data(json_data)
            client = json.loads(api.send_request('crm', 'api/data/' + json_data['client_id']))[0]
            print(client)
            if client:
                reduction = client['fidelityPoint'] // 20

            body = {
                'name': str(order_sum - reduction)
            }
            api.post_request('gestion-paiement', 'gestion-paiement/proceed-payement', body)
        else:
            database_update()

    products = Article.objects.all()

    time = api.send_request('scheduler', 'clock/time')
    helloworld = api.send_request('gestion-magasin', 'hello')
    string = 'Il est'
    final_price = order_sum - reduction

    context = {
        'time': time,
        'helloworld': helloworld,
        'string': string,
        'products': products,
        'sum': order_sum,
        'client': client,
        'reduction': reduction,
        'final_price': final_price
    }

    return render(request, 'index.html', context)

def load_data(json_data):
    tmp = []
    for list_product in json_data["list_product"]:
        for list in list_product["list"]:
            tmp.append(list)
    return compute_price(tmp)

def compute_price(data):
    sum = 0
    for elt in data:
        sum += Article.objects.get(name=elt).price
    return sum

@csrf_exempt
def scheduler(request):

    schedule_result = ""

    if request.method == "POST":
        time = (request.POST.get("time") + ":00").replace('-', '/').replace('T', '-')
        date = time.split('/')
        day = date[2].split('-')
        final_time_str = day[0] + '/' + date[1] + '/' + date[0] + '-' + day[1]
        final_time = datetime.strptime(final_time_str, '%d/%m/%Y-%H:%M:%S')
        time_str = final_time.strftime('%d/%m/%Y-%H:%M:%S')
        print(time_str)
    #    body = {"target_url": "database_update", "target_app": "caisse", "time": time_str, "recurrence": "day", "data": "",
     #           "source_app": "caisse", "name": "task1"}

        body = {"target_url": "database_update", "target_app": "caisse", "time": final_time, "recurrence": "day", "data": "", "source_app": "caisse", "name": "random"}
        print(body)
     #   schedule_result = api.post_request("scheduler", "schedule/add", body)
        schedule_task("caisse", "database_update", final_time, "day", "", "caisse", "update_database2")

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

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text