from django.urls import path
from . import views

urlpatterns = [
    # Ruta raíz: Muestra el formulario de registro
    path('', views.registro_view, name='registro'),
    
    # Ruta del lector: Muestra la interfaz de la cámara
    path('lector/', views.lector_view, name='lector'),
    
    # API: Procesa la petición asíncrona del escáner
    path('api/procesar-qr/', views.procesar_qr, name='procesar_qr'),
]