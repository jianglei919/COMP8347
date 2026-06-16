# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('vulnerable/', views.vulnerable_article, name='vulnerable_article'),
    path('safe_param/', views.safe_article_param, name='safe_article_param'),
    path('safe_orm/', views.safe_article_orm, name='safe_article_orm'),
]
