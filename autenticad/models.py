from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from .validators import validate_whatsapp

# Gerenciador personalizado para o modelo CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido.')
        if not nickname:
            raise ValueError('O nickname deve ser fornecido.')
        
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(nickname, email, password, **extra_fields)

# Modelo CustomUser que estende AbstractUser
class CustomUser(AbstractUser):
    # Removendo o campo username herdado
    username = None
    whatsapp = models.CharField(max_length=15, blank=True, null=True, validators=[validate_whatsapp])


    # Atualização da hierarquia de níveis
    HIERARCHY_LEVELS = [
        (1, 'Básico'),
        (2, 'Autoral'),
        (3, 'Escola'),
        (4, 'Ritinha'),
        (5, 'Amigos'),
        (6, 'Família'),
    ]
    
    level = models.PositiveSmallIntegerField(choices=HIERARCHY_LEVELS, default=1)  # Nível do usuário
    user_level = models.PositiveSmallIntegerField(choices=HIERARCHY_LEVELS, default=1)  # Nível do usuário (usuário comum)
    nickname = models.CharField(max_length=30, unique=True)  # Campo nickname obrigatório e único
    
    # Campos adicionais
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Campo de avatar
    age = models.PositiveIntegerField(blank=True, null=True)  # Campo de idade
    birth_date = models.DateField(blank=True, null=True)  # Campo de data de nascimento
    city = models.CharField(max_length=100, blank=True, null=True)  # Campo de cidade
    biography = models.TextField(blank=True, null=True)  # Campo de biografia
    how_you_know = models.TextField(blank=True, null=True)  # Campo de como conhece

    # Campos adicionais
    whatsapp = models.CharField(max_length=15, blank=True, null=True)  # Campo de WhatsApp
    state = models.CharField(max_length=100, blank=True, null=True)  # Campo de estado
    address = models.TextField(blank=True, null=True)  # Campo de endereço

    # Relacionamentos
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.',
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário'
    )

    USERNAME_FIELD = 'nickname'  # Define 'nickname' como o campo de login
    REQUIRED_FIELDS = ['email']  # Define o email como obrigatório

    objects = CustomUserManager()  # Gerenciador de usuários personalizado

    def __str__(self):
        return self.nickname
