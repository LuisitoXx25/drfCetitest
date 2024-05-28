from rest_framework import serializers
from .models import Programmer, Prediccion

class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Programmer
        fields='__all__'

class PrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediccion
        fields = ('respuestas', 'resultados')