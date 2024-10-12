from django.urls import path
from .views import register, user_login, user_logout, dashboard

urlpatterns = [
    path('register/', register, name='register'),      # URL para o registro de usuários
    path('login/', user_login, name='login'),          # URL para login
    path('logout/', user_logout, name='logout'),       # URL para logout
    path('dashboard/', dashboard, name='dashboard'),   # URL para a dashboard
]
