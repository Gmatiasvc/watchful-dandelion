import hashlib
import qrcode
import io
import base64
import time
import json
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Importaciones locales (asegúrate de que forms.py y models.py estén en la carpeta core)
from .forms import RegistroPersonaForm
from .models import Asistencia

# -------------------------------------------------------------------------
# Funciones Auxiliares
# -------------------------------------------------------------------------

def generar_hash(nombre, apellido, documento):
    """
    Genera un hash SHA256 único basado en los datos del usuario.
    Replica la lógica original de tu script qr_generator.py
    """
    to_hash = f"{nombre}{apellido}{documento}"
    hashed = hashlib.sha256(to_hash.encode()).hexdigest()
    return hashed

# -------------------------------------------------------------------------
# Vistas (Views)
# -------------------------------------------------------------------------

def registro_view(request):
    """
    Maneja el formulario de registro:
    1. Recibe datos (Nombre, Apellido, DNI).
    2. Genera el hash.
    3. Guarda en base de datos si no existe.
    4. Genera el código QR en memoria y lo muestra en la web.
    """
    qr_image_base64 = None
    hash_generado = None
    nombre_completo = None

    if request.method == 'POST':
        form = RegistroPersonaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            documento = form.cleaned_data['documento']
            
            # 1. Generar Hash
            hash_id = generar_hash(nombre, apellido, documento)
            
            # 2. Guardar en BD (get_or_create evita duplicados)
            # time_entry y time_exit se inicializan en 0 según tu esquema SQL
            obj, created = Asistencia.objects.get_or_create(
                id_hash=hash_id,
                defaults={'time_entry': 0, 'time_exit': 0}
            )

            if created:
                messages.success(request, 'Usuario registrado exitosamente en la base de datos.')
            else:
                messages.info(request, 'El usuario ya existía. Se ha regenerado su código QR visual.')

            # 3. Generar QR (usando librería qrcode)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L, # type: ignore
                box_size=10,
                border=4,
            )
            qr.add_data(hash_id)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Guardar imagen en buffer de memoria (no en disco) para mostrarla en HTML
            buffer = io.BytesIO()
            img.save(buffer, format="PNG") # type: ignore
            qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            hash_generado = hash_id
            nombre_completo = f"{nombre} {apellido}"

    else:
        form = RegistroPersonaForm()

    return render(request, 'core/registro.html', {
        'form': form,
        'qr_image': qr_image_base64,
        'hash_id': hash_generado,
        'nombre': nombre_completo
    })

def lector_view(request):
    """
    Simplemente renderiza la plantilla HTML que contiene el lector de cámara (JavaScript).
    """
    return render(request, 'core/lector.html')

# -------------------------------------------------------------------------
# API Endpoints (Lógica del Escáner)
# -------------------------------------------------------------------------

@csrf_exempt
def procesar_qr(request):
    """
    API que recibe una petición POST con el JSON {'hash_id': '...'}.
    Ejecuta la lógica de Entrada/Salida similar a database.py -> entryAction.
    """
    if request.method == 'POST':
        try:
            # 1. Parsear datos
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
                
            hashed = data.get('hash_id')
            
            if not hashed:
                return JsonResponse({'status': 'error', 'message': 'Hash no proporcionado'}, status=400)

            # 2. Buscar usuario
            try:
                registro = Asistencia.objects.get(id_hash=hashed)
            except Asistencia.DoesNotExist:
                return JsonResponse({'status': 'not_found', 'message': 'Usuario no encontrado en base de datos'}, status=404)

            # 3. Lógica de Negocio (Entrada vs Salida)
            ts_ahora = int(time.time()) # Timestamp Unix actual
            dt_ahora = datetime.fromtimestamp(ts_ahora).strftime("%Y-%m-%d %H:%M:%S")

            # Caso A: No tiene entrada registrada -> Registrar Entrada
            if registro.time_entry == 0:
                registro.time_entry = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'entrada', 
                    'message': f'Entrada registrada: {dt_ahora}'
                })
            
            # Caso B: Ya tiene entrada, pero no salida -> Registrar Salida
            elif registro.time_exit == 0:
                registro.time_exit = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'salida', 
                    'message': f'Salida registrada: {dt_ahora}'
                })
            
            # Caso C: Ya tiene ambas -> Informar que ya completó
            else:
                return JsonResponse({
                    'status': 'info', 
                    'type': 'completado', 
                    'message': 'El ciclo de asistencia (entrada/salida) ya fue completado.'
                })

        except Exception as e:
            # Captura cualquier otro error inesperado
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # Si no es POST
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)