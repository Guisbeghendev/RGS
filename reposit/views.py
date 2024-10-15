from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Gallery, Image, Comment  # Certifique-se de que o modelo Comment está importado
from PIL import Image as PILImage
from io import BytesIO

# Listagem de anos com galerias
def gallery_list(request):
    user_level = request.user.level if request.user.is_authenticated else 1
    galleries = Gallery.objects.filter(level__lte=user_level)
    
    # Verifica se o parâmetro de ordem foi passado na URL
    order = request.GET.get('order', 'desc')  # 'desc' é o padrão
    if order == 'asc':
        years = galleries.dates('event_date', 'year', order='ASC')  # Ordenação crescente
    else:
        years = galleries.dates('event_date', 'year', order='DESC')  # Ordenação decrescente

    # Paginação dos anos (10 anos por página)
    paginator = Paginator(years, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reposit/gallery_list.html', {
        'page_obj': page_obj, 
        'galleries': galleries,
        'current_order': order  # Passando o estado atual da ordem para o template
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

# Visualizar imagem com marca d'água virtual
def gallery_image_view(request, image_id):
    img_instance = get_object_or_404(Image, id=image_id)

    # Abrir a imagem original
    with PILImage.open(img_instance.image.path) as img:
        if img_instance.gallery.watermark:  # Verificar se há marca d'água
            watermark = PILImage.open(img_instance.gallery.watermark.image.path).convert("RGBA")

            # **Alterar tamanho da marca d'água aqui**
            # Redimensionar a marca d'água proporcionalmente
            # Para alterar o tamanho da marca d'água, ajuste os valores (img.width // 10, img.height // 10)
            watermark = watermark.resize((img.width // 10, img.height // 10), PILImage.LANCZOS)  # Atualizado para LANCZOS

            # Posicionar no canto inferior direito
            position = (img.width - watermark.width - 10, img.height - watermark.height - 10)

            # Criar imagem combinada
            combined = PILImage.new('RGBA', img.size)
            combined.paste(img.convert("RGBA"), (0, 0))
            combined.paste(watermark, position, mask=watermark)

            # Converter para RGB para exibição
            combined = combined.convert("RGB")

            # Enviar imagem combinada na resposta HTTP
            buffer = BytesIO()
            combined.save(buffer, format='JPEG')
            buffer.seek(0)
            return HttpResponse(buffer, content_type='image/jpeg')

    # Se não houver marca d'água, retornar a imagem original
    with open(img_instance.image.path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/jpeg')
