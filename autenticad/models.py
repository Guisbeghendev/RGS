from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        if not nickname:
            raise ValueError('O nickname deve ser fornecido')
        
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

class CustomUser(AbstractUser):
    # Removendo o campo username herdado
    username = None

    # Atualização da hierarquia de níveis
    HIERARCHY_LEVELS = [
        (1, 'Básico'),
        (2, 'Autoral'),
        (3, 'Escola'),
        (4, 'Ritinha'),
        (5, 'Amigos'),
        (6, 'Família'),
    ]
    
    level = models.PositiveSmallIntegerField(choices=HIERARCHY_LEVELS, default=1)  # Definindo o nível padrão como 1
    user_level = models.PositiveSmallIntegerField(choices=HIERARCHY_LEVELS, default=1)  # Novo campo user_level
    nickname = models.CharField(max_length=30, unique=True)  # Campo nickname obrigatório e único
    
    # Novos campos a serem adicionados
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Campo de avatar
    age = models.PositiveIntegerField(blank=True, null=True)  # Campo de idade
    birth_date = models.DateField(blank=True, null=True)  # Campo de data de nascimento
    city = models.CharField(max_length=100, blank=True, null=True)  # Campo de cidade
    biography = models.TextField(blank=True, null=True)  # Campo de biografia
    how_you_know = models.TextField(blank=True, null=True)  # Campo de como conhece

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Nome relacionado para o acesso reverso
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Nome relacionado para o acesso reverso
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'nickname'  # Define 'nickname' como o campo de login
    REQUIRED_FIELDS = ['email']  # Define o email como obrigatório

    objects = CustomUserManager()  # Gerenciador de usuários personalizado

    def __str__(self):
        return self.nickname
