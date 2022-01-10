from django.shortcuts import render, redirect
from .models import Article
from rest_framework import status
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_api_practice_app.permissions import IsOwnerOrReadOnly
from .forms import NewUserForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


# Create your views here.

class SignUpView(CreateView):
    User = get_user_model()
    model = User
    success_url = reverse_lazy('rest_framework:login')
    template_name = 'sign_up.html'
    form_class = NewUserForm


@login_required(login_url='/api-auth/login/')
@api_view(['GET', 'POST'])  #list articles or create a new one
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/api-auth/login/')
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)