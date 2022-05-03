from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    # path('', views.lista_login, name='lista_login'),
    path('login/', views.lista_login, name='lista_login'),
    path('logout/', views.lista_logout, name='lista_logout'),
    path('registrar/', views.lista_registro, name='lista_registro'),
    path('add_contato/', views.lista_add_contato, name='lista_add_contato'),
]
