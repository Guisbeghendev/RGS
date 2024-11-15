# urls.py do subapp profilegs
from django.urls import path
from .views import ProfileView, edit_profile, delete_account

app_name = 'profilegs'  # Define o namespace para este subapp

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),  # URL para visualizar o perfil
    path('profile/edit/', edit_profile, name='edit_profile'),  # URL para editar o perfil
    path('profile/delete/', delete_account, name='delete_account'),  # URL para deletar a conta
]
