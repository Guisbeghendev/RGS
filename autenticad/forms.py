from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(required=False, max_length=30, label='Primeiro Nome')
    surname = forms.CharField(required=False, max_length=30, label='Sobrenome')
    nickname = forms.CharField(
        required=True,
        max_length=30,
        label='Nome de Usuário',
        error_messages={'required': 'Este campo é obrigatório.'}
    )
    email = forms.EmailField(
        required=True,
        label='E-mail',
        error_messages={'required': 'Este campo é obrigatório.'}
    )
    age = forms.IntegerField(required=False, label='Idade')
    birth_date = forms.DateField(
        required=False,
        label='Data de Nascimento',
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
    city = forms.CharField(required=False, max_length=50, label='Cidade')
    state = forms.CharField(required=False, max_length=50, label='Estado')
    address = forms.CharField(required=False, max_length=100, label='Endereço')
    whatsapp = forms.CharField(required=False, max_length=15, label='WhatsApp')
    avatar = forms.ImageField(required=False, label='Foto para Avatar')
    biography = forms.CharField(required=False, widget=forms.Textarea, label='Biografia')
    how_you_know = forms.CharField(required=False, widget=forms.Textarea, label='Como você me conhece?')

    class Meta:
        model = CustomUser
        fields = (
            'name', 'surname', 'nickname', 'email', 'password1', 'password2',
            'age', 'birth_date', 'city', 'state', 'address', 'whatsapp',
            'avatar', 'biography', 'how_you_know'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data['nickname']
        user.email = self.cleaned_data['email']
        user.level = 1  # Define o nível padrão como 1
        
        if commit:
            user.save()
        return user
