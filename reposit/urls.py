# reposit/urls.py

from django.urls import path
from . import views

app_name = 'reposit_n1'

urlpatterns = [
    # Listagem de galerias
    path('gallery_list/', views.gallery_list, name='gallery_list'),

    # Exibir galerias por ano
    path('year/<int:year>/', views.gallery_by_year, name='gallery_by_year'),

    # Detalhes de uma galeria específica
    path('gallery/<int:gallery_id>/', views.gallery_detail, name='gallery_detail'),

    # Processar likes em uma imagem via AJAX
    path('like/<int:image_id>/', views.like_image, name='like_image'),
]
