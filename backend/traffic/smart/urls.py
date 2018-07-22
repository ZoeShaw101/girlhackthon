from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trails/', views.trails, name='trails'),
    path('bestendplace/', views.bestEndPalce, name='bestendplace'),
    path('geohashsearch/', views.GeoHashSearch, name='geohashsearch')
]