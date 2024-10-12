# reposit/admin.py

from django.contrib import admin
from .models import Gallery, Image, Comment, Watermark
from django import forms
from multiupload.fields import MultiFileField  # Importando MultiFileField

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Definindo como 0 para não mostrar campos vazios

class GalleryForm(forms.ModelForm):
    images = MultiFileField(required=False)  # Alterando para MultiFileField

    class Meta:
        model = Gallery
        fields = '__all__'

    def save(self, commit=True):
        gallery = super().save(commit=False)  # Não salve ainda
        if commit:
            gallery.save()  # Salve a galeria primeiro
        if self.cleaned_data['images']:
            for image_file in self.cleaned_data['images']:
                Image.objects.create(gallery=gallery, image=image_file)
        return gallery

class GalleryAdmin(admin.ModelAdmin):
    form = GalleryForm
    inlines = [ImageInline]
    exclude = ('total_likes',)  # Exclui o campo de likes do formulário

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Watermark)
