from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'programmers', views.ProgrammerViewSet)
router.register(r'prediccion', views.PrediccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('realizar-prediccion/', views.realizar_prediccion, name='realizar_prediccion')
]
