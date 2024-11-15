"""
Configuração de URL para projeto GuiSbeghen.

A lista `urlpatterns` roteia URLs para visualizações. Para mais informações consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Exemplos:
Visualizações de função
    1. Adicione uma importação: das visualizações de importação my_app
    2. Adicione um URL aos urlpatterns: path('', views.home, name='home')
Visualizações baseadas em classe
    1. Adicione uma importação: from other_app.views import Home
    2. Adicione um URL aos urlpatterns: path('', Home.as_view(), name='home')
Incluindo outro URLconf
    1. Importe a função include(): from django.urls import include, path
    2. Adicione um URL aos urlpatterns: path('blog/', include('blog.urls'))
"""

# urls.py do projeto principal
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Inclui as URLs do subapp home
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('autenticad/', include('autenticad.urls')),
    path('sobregs/', include('sobregs.urls', namespace='sobregs')),  # Namespace correto aqui

    # Incluindo as URLs do subapp profilegs
    path('profilegs/', include('profilegs.urls', namespace='profilegs')),  # Corrigido para usar 'profilegs'

    # Repositório Nível 1
    path('reposit/n1/', include('reposit.urls', namespace='reposit_n1')),

    # Preparação para os outros níveis (futuro)
    # path('reposit/n2/', include('reposit_n2.urls', namespace='reposit_n2')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
