from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('catalog', views.Cataloge.as_view(), name='catalog'),
    path('search', views.Catalog().handle_search, name='search'),
    path('filter', views.Catalog().handle_filtering, name='filter'),
    path('pensioner/<str:discount>', views.Catalog().pensioners, name='pensioner'),
    path('store/<int:pk>', views.Store.as_view(), name='store'),
    path('map', views.Map.as_view(), name='map'),
    path('about', views.About.as_view(), name='about'),
    path('news', views.News.as_view(), name='news'),
    #path('shop', s.shop_map, name='shop'),
    path('my_view/', views.JsonFilterMoviesView.as_view(), name='my_view'),
    # path('', views.FeedbackView.as_view()),
]