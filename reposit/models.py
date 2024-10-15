from django.db import models
from django.conf import settings
import os
import uuid

HIERARCHY_LEVELS = [
    (1, 'Básico'),
    (2, 'Autoral'),
    (3, 'Escola'),
    (4, 'Ritinha'),
    (5, 'Amigos'),
    (6, 'Família'),
]

def generate_image_filename(instance, filename):
    """Gera um nome único para a imagem, preservando sua extensão."""
    ext = filename.split('.')[-1]  # Pega a extensão do arquivo
    filename = f"{uuid.uuid4()}.{ext}"  # Exemplo: '4f2a8d1b-9f13-4c1a.jpg'
    return os.path.join('gallery_images/', filename)

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    total_likes = models.PositiveIntegerField(default=0)
    watermark = models.ForeignKey('Watermark', null=True, blank=True, on_delete=models.SET_NULL)
    level = models.PositiveSmallIntegerField(choices=HIERARCHY_LEVELS, default=1)

    def update_total_likes(self):
        """Atualiza o total de likes da galeria com base nas imagens relacionadas.""" 
        self.total_likes = sum(image.likes for image in self.images.all())
        self.save()

    def __str__(self):
        return self.title

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_image_filename)  # Renomeia automaticamente
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Image in {self.gallery.title} (Likes: {self.likes})'

class Comment(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.gallery}'

class Watermark(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='watermarks/')

    def __str__(self):
        return self.name
