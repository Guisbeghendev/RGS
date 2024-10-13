from django.urls import path
from .views import sobregs_home

# Define o namespace para evitar o erro de 'NoReverseMatch'
app_name = 'sobregs'  

urlpatterns = [
    path('', sobregs_home, name='sobregs-home'),  # Nome mantido como 'sobregs-home'
]
