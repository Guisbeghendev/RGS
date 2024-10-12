from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # A URL raiz chama a view "index"
]
