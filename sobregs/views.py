from django.shortcuts import render

def sobregs_home(request):
    return render(request, 'sobregs/sobregs.html')
