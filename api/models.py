from django.db import models

# Create your models here.
class Programmer(models.Model):
    fullname=models.CharField(max_length=100)
    nickname=models.CharField(max_length=50)
    age= models.PositiveSmallIntegerField()
    
class Prediccion(models.Model):
    respuestas=models.CharField(max_length=500)
    resultados=models.CharField(max_length=100)
    
    def __str__(self):
        return f"Predicción {self.id}"
