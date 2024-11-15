from django import forms
from autenticad.models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'nickname', 'avatar', 'age', 'birth_date',
            'city', 'state', 'address', 'whatsapp', 
            'biography', 'how_you_know'
        ]  # Todos os campos que deseja permitir a edição
