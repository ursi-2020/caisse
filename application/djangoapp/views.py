import requests
from django.http import HttpResponse, JsonResponse
from apipkg import api_manager as api
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.core import serializers

from .models import Article, Ticket, ArticlesList
from django.utils import timezone
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
    fidelity_points = 0

    if request.method == "POST":
        if 'products' in request.POST:
          return database(request)
        elif 'delete_products' in request.POST:
            Article.objects.all().delete()
        elif 'tickets' in request.POST:
          return tickets(request)
        elif 'delete_tickets' in request.POST:
            Ticket.objects.all().delete()
        elif 'scheduler' in request.POST:
            return scheduler(request)
        elif 'order' in request.POST and request.FILES and request.FILES['file']:
            try:
                json_data = json.loads(request.FILES['file'].read())
            except Exception as e:
                return HttpResponse("Error in products update : " + str(e))
            sales(json_data)
        elif 'order' in request.POST:
            return HttpResponse("File not found")
        else:
            database_update()

    final_price = order_sum - reduction

    context = {
        'sum': order_sum,
        'fidelity_points': fidelity_points,
        'client': client,
        'reduction': reduction,
        'final_price': final_price
    }

    return render(request, 'index.html', context)


def sales(json_data):
    if "tickets" in json_data:
        for ticket in json_data["tickets"]:
            if "panier" in ticket:
                sum = 0
                articles = []
                for product in ticket["panier"]:
                    quantity = product["quantity"]
                    article = Article.objects.get(codeProduit=product["codeProduit"])
                    article_list = ArticlesList(codeProduit=article.codeProduit, quantite=quantity)
                    article_list.save()
                    articles.append(article_list)
                    sum += (quantity * article.prix)
                client = ""
                if "carteFid" in ticket:
                    client = json.loads(api.send_request('gestion-magasin', 'api/customers/?account=' + ticket["carteFid"]))["account"]

                mode_paiement = "CASH"
                if ticket["modePaiement"] == "CARD":
                    card = ticket["card"]
                    mode_paiement = "CARD"
                    body = {
                        'amount': sum,
                        'payement_method': mode_paiement,
                        'client_id': client,
                        'card': card
                    }
                    paiement = api.post_request('gestion-paiement', 'api/proceed-payement', body)
                    if paiement != 200:
                        return


                new_ticket = Ticket(date=timezone.now(), prix=sum, client=client, pointsFidelite=0, modePaiement=mode_paiement)
                new_ticket.save()
                new_ticket.articles.set(articles)
                new_ticket.save()


@require_GET
def get_tickets(request):
    tickets = Ticket.objects.all()
    data = json.loads(serializers.serialize('json', tickets))
    response = []
    for ticket_json in data:
        ticket = ticket_json["fields"]
        articles_code = []
        for article in ticket['articles']:
            current = ArticlesList.objects.get(id=article)
            json_article = {'codeProduit': current.codeProduit, 'quantity': current.quantite}
            articles_code.append(json.loads(json.dumps(json_article)))
        ticket['articles'] = articles_code
        response.append(ticket)

    return JsonResponse(response, safe=False)

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
    products = Article.objects.all().values()
    for product in products:
        product.update(prix=product['prix'] / 100)
    context = {
        'products': products
    }

    return render(request, 'database.html', context)

def tickets(request):
    tickets = Ticket.objects.all()
    for ticket in tickets:
        ticket.prix = ticket.prix / 100
    context = {
        'tickets': tickets
    }

    return render(request, 'tickets.html', context)

@csrf_exempt
def database_update():
    Article.objects.all().delete()
    data = ""
    try:
        data = api.send_request("gestion-magasin", "api/products")
    except Exception as e:
        return HttpResponse("Error in database update" + str(e))

    try:
        json_data = json.loads(data)
    except Exception as e:
        return HttpResponse("Error in database update" + str(e))

    try:
        for product in json_data:
            article = Article(codeProduit=product["codeProduit"], prix=product["prix"], stock=product["quantiteMin"])
            article.save()
    except Exception as e:
        return HttpResponse("Error in the load of the items" + str(e))

@csrf_exempt
def database_update_scheduled(request):
    Article.objects.all().delete()

    data = ""
    try:
        data = api.send_request("gestion-magasin", "api/products")
    except Exception as e:
        return HttpResponse("Error in database update scheduled : " + str(e))

    try:
        json_data = json.loads(data)
    except Exception as e:
        return HttpResponse("Error in database update scheduled : " + str(e))

    for product in json_data:
        article = Article(codeProduit=product["codeProduit"], prix=product["prix"] / 100, stock=product["quantiteMin"])
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