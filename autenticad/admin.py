from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos no formulário de edição de usuários
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Nível de Usuário'), {'fields': ('level',)}),  # Exibe o nível no admin
    )
    
    # Campos a serem exibidos no formulário de adição de novos usuários
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'password1', 'password2', 'level'),
        }),
    )
    
    # Configurações de exibição na lista de usuários
    list_display = ['nickname', 'email', 'level', 'is_staff', 'is_active']
    list_filter = ['level', 'is_staff', 'is_active']
    search_fields = ('nickname', 'email')
    ordering = ('nickname',)

# Registra o CustomUserAdmin no admin
admin.site.register(CustomUser, CustomUserAdmin)
