from django.db import models


class Article(models.Model):
    codeProduit = models.CharField(max_length=20)
    stock = models.PositiveIntegerField()
    prix = models.IntegerField()
    def __str__(self):
        return '{}'.format(self.name)

class Ticket(models.Model):
    date = models.DateTimeField()
    prix = models.IntegerField()
    client = models.CharField(max_length=20)
    articles = models.ManyToManyField(Article)
    pointsFidelite = models.IntegerField()
    modePaiement = models.CharField(max_length=10)