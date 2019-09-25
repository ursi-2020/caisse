from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()
    price = models.FloatField()
    def __str__(self):
        return '{}'.format(self.name)
