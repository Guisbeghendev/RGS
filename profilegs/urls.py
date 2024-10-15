# profilegs/urls.py

from django.urls import path
from .views import profilegs_view

app_name = 'profilegs'  

urlpatterns = [
    path('', profilegs_view, name='profilegs'),  # Verifique se o nome é 'profilegs'
]
