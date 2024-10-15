# reposit/admin.py

from django.contrib import admin
from .models import Gallery, Image, Comment, Watermark
from django import forms
from multiupload.fields import MultiFileField
from PIL import Image as PILImage
import os

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Não exibe campos extras vazios

class GalleryForm(forms.ModelForm):
    images = MultiFileField(required=False)  # Permite múltiplos uploads

    class Meta:
        model = Gallery
        fields = '__all__'

    def save(self, commit=True):
        gallery = super().save(commit=False)  # Não salva ainda
        if commit:
            gallery.save()  # Salva a galeria primeiro

        # Adiciona lógica para renomear imagens durante o upload
        if self.cleaned_data['images']:
            for image_file in self.cleaned_data['images']:
                Image.objects.create(gallery=gallery, image=image_file)

        return gallery

class GalleryAdmin(admin.ModelAdmin):
    form = GalleryForm
    inlines = [ImageInline]
    exclude = ('total_likes',)  # Remove o campo 'total_likes' do formulário

class ImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, change):
        # Após salvar a imagem, aplique a marca d'água
        super().save_model(request, obj, change)
        self.apply_watermark(obj)

    def apply_watermark(self, image_instance):
        # Abrir a imagem original
        with PILImage.open(image_instance.image.path) as img:
            if image_instance.gallery.watermark:  # Verificar se há marca d'água
                watermark = PILImage.open(image_instance.gallery.watermark.image.path).convert("RGBA")

                # Redimensionar a marca d'água
                watermark = watermark.resize((img.width // 10, img.height // 10), PILImage.LANCZOS)  # Ajuste conforme necessário

                # Posicionar no canto inferior direito
                position = (img.width - watermark.width - 10, img.height - watermark.height - 10)

                # Criar imagem combinada
                combined = PILImage.new('RGBA', img.size)
                combined.paste(img.convert("RGBA"), (0, 0))
                combined.paste(watermark, position, mask=watermark)

                # Converter para RGB para salvar
                combined = combined.convert("RGB")

                # Salvar a nova imagem
                combined.save(image_instance.image.path, format='JPEG')  # Substitui a imagem original

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)
admin.site.register(Watermark)
