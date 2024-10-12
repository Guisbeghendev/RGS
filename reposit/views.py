# reposit/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Gallery, Image, Comment

# Listagem de anos com galerias
def gallery_list(request):
    galleries = Gallery.objects.all()
    years = galleries.dates('event_date', 'year', order='DESC')
    return render(request, 'reposit/gallery_list.html', {'years': years, 'galleries': galleries})

# Exibir todas as galerias de um ano específico
def gallery_by_year(request, year):
    galleries = Gallery.objects.filter(event_date__year=year)
    return render(request, 'reposit/gallery_by_year.html', {'galleries': galleries, 'year': year})

# Visualizar detalhes da galeria, incluindo imagens, likes e comentários
def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)

    if request.method == 'POST':
        # Processar comentário
        comment_content = request.POST.get('comment')
        if comment_content:
            comment = Comment(gallery=gallery, user=request.user, content=comment_content)
            comment.save()
            return redirect('reposit_n1:gallery_detail', gallery_id=gallery.id)

    return render(request, 'reposit/gallery_detail.html', {
        'gallery': gallery,
    })

# Processar o like de uma imagem via requisição AJAX
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
