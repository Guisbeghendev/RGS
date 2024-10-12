from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser  # Certifique-se de importar seu modelo CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Inclui FILES para o avatar
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro realizado com sucesso! Você pode fazer login agora.')
            return redirect('login')  # Redirecionar após o registro
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'autenticad/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        user = CustomUser.objects.filter(nickname=nickname).first()
        if user and user.check_password(password):
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')  # Aqui você está redirecionando para a URL correta
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    form = AuthenticationForm()
    return render(request, 'autenticad/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('login')  # Redireciona para a página de login após o logout

@login_required
def dashboard(request):
    return render(request, 'autenticad/dashboard.html')
