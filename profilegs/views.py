from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profilegs_view(request):
    user = request.user  # Recupera o usuário autenticado
    return render(request, 'profilegs/profilegs.html', {
        'user': user,  # Passando o usuário inteiro
    })
