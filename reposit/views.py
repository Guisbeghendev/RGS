# reposit/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Gallery, Image, Comment

# Listagem de anos com galerias
def gallery_list(request):
    galleries = Gallery.objects.all()
    years = galleries.dates('event_date', 'year', order='DESC')
    return render(request, 'reposit/gallery_list.html', {'years': years})

# Exibir todas as galerias de um ano específico
def gallery_by_year(request, year):
    galleries = Gallery.objects.filter(event_date__year=year)
    return render(request, 'reposit/gallery_by_year.html', {'galleries': galleries, 'year': year})

# Visualizar detalhes da galeria, incluindo imagens, likes e comentários
def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    images = gallery.images.all()
    comments = gallery.comments.all()

    if request.method == 'POST':
        # Processar comentário
        comment_content = request.POST.get('comment')
        if comment_content:
            comment = Comment(gallery=gallery, user=request.user, content=comment_content)
            comment.save()
            return redirect('gallery_detail', gallery_id=gallery.id)

    return render(request, 'reposit/gallery_detail.html', {
        'gallery': gallery,
        'images': images,
        'comments': comments
    })

# Processar o like de uma imagem via requisição AJAX
@csrf_exempt  # Exime a view da verificação de CSRF para facilitar as requisições via AJAX
def like_image(request, image_id):
    if request.method == 'POST':
        # Obtém a imagem com base no ID passado
        image = get_object_or_404(Image, id=image_id)
        
        # Incrementa o número de likes
        image.likes += 1
        image.save()

        # Retorna o número atualizado de likes no formato JSON
        return JsonResponse({'likes': image.likes})

    return JsonResponse({'error': 'Invalid request'}, status=400)
