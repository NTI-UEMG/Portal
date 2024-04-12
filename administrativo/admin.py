from django.contrib import admin
from .models import Papel, Curso

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'coordenador', 'descricao')
    fields = ['nome', 'coordenador', 'descricao', 'imagem']
    
admin.site.register(Papel)
admin.site.register(Curso, CursoAdmin)
