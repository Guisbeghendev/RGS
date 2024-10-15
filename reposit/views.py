# reposit/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Gallery, Image, Comment

# Listagem de anos com galerias
def gallery_list(request):
    user_level = request.user.level if request.user.is_authenticated else 1
    galleries = Gallery.objects.filter(level__lte=user_level)
    years = galleries.dates('event_date', 'year', order='DESC')

    # Paginação dos anos (10 anos por página)
    paginator = Paginator(years, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reposit/gallery_list.html', {
        'page_obj': page_obj, 
        'galleries': galleries
    })

# Exibir todas as galerias de um ano específico com paginação
def gallery_by_year(request, year):
    user_level = request.user.level if request.user.is_authenticated else 1
    galleries = Gallery.objects.filter(event_date__year=year, level__lte=user_level)

    # Paginação das galerias do ano (10 galerias por página)
    paginator = Paginator(galleries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reposit/gallery_by_year.html', {
        'page_obj': page_obj, 
        'year': year
    })

# Visualizar detalhes da galeria
def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    user_level = request.user.level if request.user.is_authenticated else 1

    if gallery.level > user_level:
        return render(request, 'reposit/403.html')

    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        if comment_content:
            Comment.objects.create(gallery=gallery, user=request.user, content=comment_content)
            return redirect('reposit_n1:gallery_detail', gallery_id=gallery.id)

    return render(request, 'reposit/gallery_detail.html', {'gallery': gallery})

# Processar o like de uma imagem via AJAX
@csrf_exempt
def like_image(request, image_id):
    if request.method == 'POST':
        try:
            image = get_object_or_404(Image, id=image_id)
            image.likes += 1
            image.save()
            return JsonResponse({'likes': image.likes})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
