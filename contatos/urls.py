from django.urls import path

from . import views

app_name = 'contatos'
urlpatterns = [
    path('', views.index, name='index'),
    path('busca/', views.busca, name='busca'),
    path('<int:contato_id>', views.ver_contato, name='ver_contato'),
    path('delete/<int:contato_id>', views.deleta_contato, name="deleta-contato"),
]
