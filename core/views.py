import hashlib
import qrcode
import io
import base64
import time
import json
import pytz # type: ignore
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Importaciones locales
from .forms import RegistroPersonaForm
from .models import Asistencia

# -------------------------------------------------------------------------
# Funciones Auxiliares
# -------------------------------------------------------------------------

def generar_hash(nombre, apellido, documento):
    """
    Genera un hash SHA256 único basado en los datos del usuario.
    """
    to_hash = f"{nombre}{apellido}{documento}"
    hashed = hashlib.sha256(to_hash.encode()).hexdigest()
    return hashed

def obtener_hora_local(timestamp):
    """
    Convierte un timestamp Unix a la zona horaria configurada en settings.
    """
    dt_utc = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    tz_local = pytz.timezone(settings.TIME_ZONE)
    return dt_utc.astimezone(tz_local).strftime("%Y-%m-%d %H:%M:%S")

# -------------------------------------------------------------------------
# Vistas (Views)
# -------------------------------------------------------------------------

def registro_view(request):
    """
    Maneja el formulario de registro:
    1. Recibe datos (Nombre, Apellido, DNI).
    2. Genera el hash.
    3. Guarda datos legibles y hash en BD.
    4. Genera el código QR visual.
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
            
            # 2. Guardar en BD
            # MEJORA: Ahora guardamos también los datos personales para reportes
            obj, created = Asistencia.objects.get_or_create(
                id_hash=hash_id,
                defaults={
                    'time_entry': 0, 
                    'time_exit': 0,
                    'nombre': nombre,
                    'apellido': apellido,
                    'documento': documento
                }
            )

            # Si ya existía pero no tenía los datos personales (registros antiguos), los actualizamos
            if not created and (not obj.nombre or not obj.documento):
                obj.nombre = nombre
                obj.apellido = apellido
                obj.documento = documento
                obj.save()

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
    return render(request, 'core/lector.html')

# -------------------------------------------------------------------------
# API Endpoints (Lógica del Escáner)
# -------------------------------------------------------------------------

@csrf_exempt
def procesar_qr(request):
    """
    API que recibe una petición POST con el JSON {'hash_id': '...'}.
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

            # MEJORA: Usar nombre real si está disponible
            nombre_usuario = registro.nombre if registro.nombre else "Usuario"

            # 3. Lógica de Negocio (Entrada vs Salida)
            ts_ahora = int(time.time()) # Timestamp Unix actual
            
            # Formatear hora usando la Timezone configurada
            hora_legible = obtener_hora_local(ts_ahora)

            # Caso A: No tiene entrada registrada -> Registrar Entrada
            if registro.time_entry == 0:
                registro.time_entry = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'entrada', 
                    'message': f'¡Bienvenido/a, {nombre_usuario}!\nEntrada: {hora_legible}'
                })
            
            # Caso B: Ya tiene entrada, pero no salida -> Registrar Salida
            elif registro.time_exit == 0:
                registro.time_exit = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'salida', 
                    'message': f'¡Hasta luego, {nombre_usuario}!\nSalida: {hora_legible}'
                })
            
            # Caso C: Ya tiene ambas -> Informar que ya completó
            else:
                return JsonResponse({
                    'status': 'info', 
                    'type': 'completado', 
                    'message': f'{nombre_usuario}, tu ciclo de asistencia ya fue completado hoy.'
                })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)