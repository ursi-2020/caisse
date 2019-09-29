import requests
from django.http import HttpResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Article
from datetime import datetime
import json

def index(request):
    return HttpResponse("Bienvenue sur l'appli caisse")

def helloworld(request):
    return HttpResponse("Hello,je viens de la caisse")


def products_update(request):

    order_sum = 0
    client = ''
    reduction = 0

    if request.method == "POST":
        if 'order' in request.POST and request.FILES and request.FILES['file']:
            try:
                json_data = json.loads(request.FILES['file'].read())
            except Exception as e:
                return HttpResponse("Error in products update : " + str(e))
            order_sum = load_data(json_data)
            res_request = ""
            try:
                res_request = api.send_request('gestion-magasin', 'customers/?account=' + json_data['client_account'])
            except Exception as e:
                return HttpResponse("Error in products update : " + str(e))
            try:
                client = json.loads(res_request)
            except Exception as e:
                return HttpResponse("Error in products update : " + str(e))
            if client:
                reduction = client['fidelityPoint'] // 20

            body = {
                'amount': str(order_sum - reduction)
            }
            try:
                api.post_request('gestion-paiement', 'gestion-paiement/proceed-payement', body)
            except Exception as e:
                return HttpResponse("Error in products update : " + str(e))
        elif 'order' in request.POST:
            return HttpResponse("File not found")
        else:
            database_update()

    final_price = order_sum - reduction

    context = {
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
    return round(sum, 2)


def scheduler(request):

    schedule_result = ""

    if request.method == "POST":
        time = ""
        try:
            time = (request.POST.get("time") + ":00").replace('-', '/').replace('T', '-')
        except Exception as e:
            return HttpResponse("Error in scheduler : " + str(e))
        date = time.split('/')
        day = date[2].split('-')
        final_time_str = day[0] + '/' + date[1] + '/' + date[0] + '-' + day[1]
        final_time = datetime.strptime(final_time_str, '%d/%m/%Y-%H:%M:%S')
    #    body = {"target_url": "database_update", "target_app": "caisse", "time": time_str, "recurrence": "day", "data": "",
     #           "source_app": "caisse", "name": "task1"}

        body = {"target_url": "database_update", "target_app": "caisse/", "time": final_time, "recurrence": "day", "data": "", "source_app": "caisse", "name": "random"}
     #   schedule_result = api.post_request("scheduler", "schedule/add", body)
        schedule_task("caisse", "database_update_scheduled", final_time, "day", "", "caisse", "update_database")

    tasks = ""
    try:
        tasks = api.send_request("scheduler", "schedule/list")
    except Exception as e:
        return HttpResponse("Error in scheduler : " + str(e))

    context = {
        'request': schedule_result,
        'tasks': tasks
    }

    return render(request, 'scheduler.html', context)

def database(request):
    products = Article.objects.all()

    context = {
        'products': products
    }

    return render(request, 'database.html', context)

@csrf_exempt
def database_update():
    Article.objects.all().delete()

    data = ""
    try:
        data = api.send_request("gestion-magasin", "products")
    except Exception as e:
        return HttpResponse("Error in database update" + str(e))

    try:
        json_data = json.loads(data)
    except Exception as e:
        return HttpResponse("Error in database update" + str(e))

    try:
        for product in json_data:
            article = Article(name=product["codeProduit"], price=product["prix"] / 100, stock=0)#product["quantiteMin"])
            article.save()
    except Exception as e:
        return HttpResponse("Error in the load of the items" + str(e))

@csrf_exempt
def database_update_scheduled(request):
    Article.objects.all().delete()

    data = ""
    try:
        data = api.send_request("gestion-magasin", "products")
    except Exception as e:
        return HttpResponse("Error in database update scheduled : " + str(e))

    try:
        json_data = json.loads(data)
    except Exception as e:
        return HttpResponse("Error in database update scheduled : " + str(e))

    for product in json_data:
        article = Article(name=product["codeProduit"], price=product["prix"] / 100, stock=0)#product["quantiteMin"])
        article.save()

    return HttpResponse("Success")

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = ""
    try:
        r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    except Exception as e:
        return HttpResponse("Error in schedule_task : " + str(e))
    if r:
        print(r.status_code)
        print(r.text)
        return r.text
    else:
        return r