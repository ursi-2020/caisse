from rest_framework import serializers

from application.djangoapp.models import Article, Ticket, ArticlesList


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Article

class ArticlesListSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ArticlesList

class TicketSerializer(serializers.ModelSerializer):
    article = ArticlesListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Ticket