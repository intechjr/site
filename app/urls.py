from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView
urlpatterns = [

    #VER A LISTA DE PRODUTOS E DETALHES
    path('base/', views.base, name='base'),

    #MINHA HOME
    path('', views.home, name='home'),  

 


]
