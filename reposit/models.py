# reposit/models.py

from django.db import models
from django.conf import settings
from multiupload.fields import MultiFileField  # Importando MultiFileField

# Modelo da Galeria
class Gallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()  # Data do evento representado pela galeria
    total_likes = models.PositiveIntegerField(default=0)  # Somatória dos likes de todas as imagens
    watermark = models.ForeignKey('Watermark', null=True, blank=True, on_delete=models.SET_NULL)  # Marca d'água opcional

    def update_total_likes(self):
        """Atualiza o total de likes da galeria com base nas imagens relacionadas.""" 
        self.total_likes = sum(image.likes for image in self.images.all())
        self.save()

    def __str__(self):
        return self.title

# Modelo da Imagem
class Image(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')  # Usando ImageField para um único upload
    likes = models.PositiveIntegerField(default=0)  # Contador de likes para cada imagem

    def __str__(self):
        return f'Image in {self.gallery.title} (Likes: {self.likes})'

# Modelo de Comentário
class Comment(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL aqui
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.gallery}'

# Modelo de Marca D'água
class Watermark(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='watermarks/')

    def __str__(self):
        return self.name
