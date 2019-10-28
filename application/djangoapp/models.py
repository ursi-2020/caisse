from django.db import models


class Article(models.Model):
    codeProduit = models.CharField(max_length=20)
    stock = models.PositiveIntegerField()
    prix = models.IntegerField()

class ArticlesList(models.Model):
    codeProduit = models.CharField(max_length=20)
    quantite = models.IntegerField()
    prix = models.IntegerField()
    promo = models.IntegerField()

class Ticket(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField()
    client = models.CharField(max_length=20)
    articles = models.ManyToManyField(ArticlesList)
    pointsFidelite = models.IntegerField()
    modePaiement = models.CharField(max_length=10)