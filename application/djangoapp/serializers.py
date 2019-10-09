from rest_framework import serializers

from application.djangoapp.models import Article, Ticket


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Article

class TicketSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Ticket