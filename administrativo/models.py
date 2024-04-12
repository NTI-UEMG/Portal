from django.db import models
from django.conf import settings

class Papel(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descricao

class Curso(models.Model):
    nome = models.CharField(max_length=200)
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True)  # Campo de texto para a descrição do curso
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)  # Campo de imagem

    def __str__(self):
        return self.nome
