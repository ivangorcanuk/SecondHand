from django.contrib import admin
from django.urls import path
from . import views

s = views.Stor()
urlpatterns = [
    path('', views.index, name='home'),
    path('catalog', views.Catalog().catalog, name='catalog'),
    path('search', views.Catalog().handle_search, name='search'),
    path('filter', views.Catalog().handle_filtering, name='filter'),
    path('pensioner/<str:discount>', views.Catalog().pensioners, name='pensioner'),
    path('store/<int:id_store>', s.stor, name='store'),
    path('map', views.Map().map, name='map'),
    path('about', views.about, name='about'),
    path('news', views.news, name='news'),
    path('shop', s.shop_map, name='shop'),
    # path('', views.FeedbackView.as_view()),
]