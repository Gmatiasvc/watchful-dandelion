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
from forms import RegistroPersonaForm
from models import Asistencia

# ... (Mantén aquí las funciones generar_hash y registro_view existentes) ...

def generar_hash(nombre, apellido, documento):
    to_hash = f"{nombre}{apellido}{documento}"
    hashed = hashlib.sha256(to_hash.encode()).hexdigest()
    return hashed

def registro_view(request):
    qr_image_base64 = None
    hash_generado = None
    nombre_completo = None

    if request.method == 'POST':
        form = RegistroPersonaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            documento = form.cleaned_data['documento']
            
            hash_id = generar_hash(nombre, apellido, documento)
            
            obj, created = Asistencia.objects.get_or_create(
                id_hash=hash_id,
                defaults={'time_entry': 0, 'time_exit': 0}
            )

            if created:
                messages.success(request, 'Usuario registrado exitosamente en la base de datos.')
            else:
                messages.info(request, 'El usuario ya existía, se ha regenerado su código QR.')

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
    """Renderiza la interfaz de la cámara."""
    return render(request, 'core/lector.html')

@csrf_exempt
def procesar_qr(request):
    """
    API que recibe el hash escaneado y ejecuta la lógica de entrada/salida.
    Replica la lógica de database.py -> entryAction
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hashed = data.get('hash_id')
            
            if not hashed:
                return JsonResponse({'status': 'error', 'message': 'Hash no proporcionado'}, status=400)

            # Buscar el registro
            try:
                registro = Asistencia.objects.get(id_hash=hashed)
            except Asistencia.DoesNotExist:
                return JsonResponse({'status': 'not_found', 'message': 'Datos no encontrados'}, status=404)

            ts_ahora = int(time.time())
            dt_ahora = datetime.fromtimestamp(ts_ahora).strftime("%Y-%m-%d %H:%M:%S")

            # Lógica de estados (igual a database.py)
            if registro.time_entry == 0:
                # Registrar Entrada
                registro.time_entry = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'entrada', 
                    'message': f'Entrada registrada: {dt_ahora}'
                })
            
            elif registro.time_exit == 0:
                # Registrar Salida
                registro.time_exit = ts_ahora
                registro.save()
                return JsonResponse({
                    'status': 'success', 
                    'type': 'salida', 
                    'message': f'Salida registrada: {dt_ahora}'
                })
            
            else:
                # Ya completado
                return JsonResponse({
                    'status': 'info', 
                    'type': 'completado', 
                    'message': 'Salida ya registrada previamente'
                })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)