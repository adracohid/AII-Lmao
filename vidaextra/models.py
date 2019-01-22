from django.db import models

# Create your models here.


class Noticia(models.Model):
    titulo=models.CharField(max_length=200)
    resumen=models.TextField()
    link=models.CharField(max_length=500)
    fecha=models.CharField(max_length=50)
    def __str__(self):
        return self.titulo

class Puntuacion(models.Model):
    puntuacion=models.PositiveIntegerField()
    userid=models.PositiveIntegerField()
    noticiaid=models.PositiveIntegerField()


