from django.db import models


class Article(models.Model):
    codeProduit = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    prix = models.IntegerField()
    promo = models.IntegerField()

class ArticlesList(models.Model):
    codeProduit = models.CharField(max_length=50)
    quantite = models.IntegerField()
    prixAvant = models.IntegerField()
    prixApres = models.IntegerField()
    promoProduit = models.IntegerField()
    promoPanier = models.IntegerField()
    promoProduitClient = models.IntegerField()

class Ticket(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField()
    client = models.CharField(max_length=50)
    articles = models.ManyToManyField(ArticlesList)
    pointsFidelite = models.IntegerField()
    modePaiement = models.CharField(max_length=10)
    transmis = models.BooleanField()