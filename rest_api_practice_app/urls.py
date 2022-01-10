from django.urls import path
from rest_api_practice_app import views
from rest_api_practice_app.views import SignUpView

app_name = 'rest_api_practice_app'

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
]