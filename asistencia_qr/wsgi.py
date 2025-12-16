import os
from django.core.wsgi import get_wsgi_application

# Apunta al archivo settings dentro del paquete asistencia_qr
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistencia_qr.settings')

application = get_wsgi_application()