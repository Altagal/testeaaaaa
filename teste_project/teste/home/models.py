from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Artigo(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100, null=False, blank=False)
    texto = models.TextField()
    data_publicacao = models.DateField(default=timezone.now)
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Artigos"
        ordering = ['-titulo', '-data_publicacao']

