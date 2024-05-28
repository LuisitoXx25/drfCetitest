from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Programmer, Prediccion
from .serializers import ProgrammerSerializer, PrediccionSerializer
import tensorflow as tf
import numpy as np

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

# Cargar el modelo una vez al iniciar el servidor para evitar recargarlo en cada solicitud
MODEL_PATH = 'api//cetired.keras'
model = load_model(MODEL_PATH)

@api_view(['POST'])
def realizar_prediccion(request):
    try:
        data = request.data.get('respuestas')
        if not data:
            return Response({'error': 'La clave "respuestas" es requerida en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convertir la cadena de respuestas a una lista de números
        respuestas_list = list(map(float, data.split(',')))
        respuestas_array = np.array([respuestas_list], dtype=np.float32)  # Ajustar el tipo de dato según sea necesario

        # Realizar la predicción utilizando el modelo
        resultado_prediccion = model.predict(respuestas_array)

        # Convertir los resultados de la predicción a una lista para ser serializados
        resultado_prediccion = resultado_prediccion.tolist()

        # Convertir el resultado a una cadena
        resultado_prediccion_str = ','.join(map(str, resultado_prediccion[0]))

        # Guardar las respuestas y resultados en la base de datos
        prediccion = Prediccion.objects.create(
            respuestas=data,
            resultados=resultado_prediccion_str
        )

        serializer = PrediccionSerializer(prediccion)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'error': 'La clave "data" es requerida en el cuerpo de la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer

class PrediccionViewSet(viewsets.ModelViewSet):
    queryset = Prediccion.objects.all()
    serializer_class = PrediccionSerializer



