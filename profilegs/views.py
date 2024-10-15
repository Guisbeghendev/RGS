# profilegs/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def profilegs_view(request):
    user = request.user  # Recupera o usuário autenticado
    try:
        return render(request, 'profilegs/profilegs.html', {'user': user})
    except Exception as e:
        print(f"Erro ao renderizar o template: {e}")
        raise Http404("Template não encontrado.")
