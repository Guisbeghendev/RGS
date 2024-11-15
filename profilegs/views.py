# views.py do subapp profilegs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import ProfileForm
from autenticad.models import CustomUser

class ProfileView(View):
    @login_required  # Garantindo que apenas usuários logados acessem esta visão
    def get(self, request):
        user = request.user
        return render(request, 'profilegs/profilegs.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profilegs:profile')  # Redireciona para a página de perfil após salvar
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'profilegs/edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()  # Exclui o usuário
        return redirect('login')  # Redireciona para a página de login após excluir
    return render(request, 'profilegs/delete_account.html', {'user': user})
