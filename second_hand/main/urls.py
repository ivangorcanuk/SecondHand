from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog', views.catalog, name='catalog'),
    path('store/<int:id_store>', views.stor, name='store'),
    path('map', views.map, name='map'),
    path('all_shop', views.all_shop, name='all_shop'),
    path('login', views.login, name='login'),
    path('about', views.about, name='about'),
    path('news', views.news, name='news'),
    path('forum', views.forum, name='forum'),
    # path('', views.FeedbackView.as_view()),
]