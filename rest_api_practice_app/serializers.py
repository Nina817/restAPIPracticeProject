from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60)
    author = UserSerializer(required=False, read_only=True)
    date = serializers.DateTimeField()
    description = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

