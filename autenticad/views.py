from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser  # Import do modelo CustomUser
from reposit.models import Gallery  # Import do modelo Gallery

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Inclui avatar
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro realizado com sucesso! Você pode fazer login agora.')
            return redirect('login')
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
            return redirect('dashboard')  # Redireciona para a dashboard
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    form = AuthenticationForm()
    return render(request, 'autenticad/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('login')  # Redireciona para o login

@login_required
def dashboard(request):
    # Filtrar galerias disponíveis para o usuário
    user_galleries = Gallery.objects.filter(level__lte=request.user.level).order_by('level')

    # Log para depuração (remover em produção)
    print(f"Usuário: {request.user.nickname}, Nível: {request.user.level}")
    print(f"Galerias disponíveis: {[g.title for g in user_galleries]}")

    return render(request, 'autenticad/dashboard.html', {
        'user_galleries': user_galleries
    })
