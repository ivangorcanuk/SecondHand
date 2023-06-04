from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('store/<int:id_store>', views.stor, name='store'),
    path('map', views.Map.as_view(), name='map'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    # path('', views.FeedbackView.as_view()),
]