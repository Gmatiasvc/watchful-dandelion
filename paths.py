from django.urls import path
from url import views

urlpatterns = [
    # Vista para registrar personas (la que ya tenías)
    path('', views.registro_view, name='registro'),
    
    # Vista de la interfaz del lector
    path('lector/', views.lector_view, name='lector'),
    
    # API endpoint para procesar el QR
    path('api/procesar-qr/', views.procesar_qr, name='procesar_qr'),
]