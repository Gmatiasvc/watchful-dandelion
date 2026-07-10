from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime
import pytz
from django.conf import settings
from .models import Asistencia

from django.urls import reverse
import urllib.parse

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista
    list_display = ('get_nombre_completo', 'get_documento', 'telefono', 'get_hora_entrada', 'get_hora_salida', 'get_duracion', 'enviar_whatsapp')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'apellido', 'documento', 'telefono', 'id_hash')

    # Permitir edición rápida del teléfono
    list_editable = ('telefono',)
    
    # Filtros laterales
    list_filter = ('time_entry', 'time_exit')

    def get_nombre_completo(self, obj):
        if obj.nombre and obj.apellido:
            return f"{obj.nombre} {obj.apellido}"
        return "Usuario sin datos (Hash)"
    get_nombre_completo.short_description = "Nombre Completo"
    get_nombre_completo.admin_order_field = 'apellido'

    def get_documento(self, obj):
        return obj.documento if obj.documento else "-"
    get_documento.short_description = "DNI / Documento"

    def _format_timestamp(self, timestamp):
        if not timestamp or timestamp == 0:
            return "-"
        
        # Convertir timestamp a zona horaria local configurada en settings
        tz_local = pytz.timezone(settings.TIME_ZONE)
        dt_utc = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
        dt_local = dt_utc.astimezone(tz_local)
        
        return dt_local.strftime("%d/%m/%Y %H:%M:%S")

    def get_hora_entrada(self, obj):
        return self._format_timestamp(obj.time_entry)
    get_hora_entrada.short_description = "Entrada"
    get_hora_entrada.admin_order_field = 'time_entry'

    def get_hora_salida(self, obj):
        return self._format_timestamp(obj.time_exit)
    get_hora_salida.short_description = "Salida"
    get_hora_salida.admin_order_field = 'time_exit'

    def get_duracion(self, obj):
        if obj.time_entry > 0 and obj.time_exit > 0:
            entrada = datetime.utcfromtimestamp(obj.time_entry)
            salida = datetime.utcfromtimestamp(obj.time_exit)
            duracion = salida - entrada
            
            # Formato bonito: H horas, M minutos
            total_seconds = int(duracion.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            return f"{hours}h {minutes}m {seconds}s"
            
        elif obj.time_entry > 0:
            return format_html('<span style="color:green;">En curso...</span>')
        return "-"
    get_duracion.short_description = "Duración Estancia"

    def enviar_whatsapp(self, obj):
        # Generate the invitation link
        domain = "http://127.0.0.1:8000" # Assuming local development. Consider using request.build_absolute_uri() in a real view, but in admin it's hard to get the request without overriding changelist_view. We use a placeholder or relative if domain is unknown.
        invitation_url = f"{domain}{reverse('invitacion', args=[obj.id_hash])}"
        nombre = f"{obj.nombre} {obj.apellido}".strip() if obj.nombre else "Invitado"

        mensaje = f"¡Hola {nombre}! Aquí tienes tu invitación y código QR de acceso para el evento: {invitation_url}"
        mensaje_encoded = urllib.parse.quote(mensaje)

        # Guardamos datos en atributos data-* para que el JS los use
        telefono = obj.telefono if obj.telefono else ""

        return format_html(
            '''
            <button type="button"
                    class="button"
                    style="background-color: #25D366; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold;"
                    onclick="sendWhatsApp(this)"
                    data-telefono="{}"
                    data-mensaje="{}">
                Enviar WhatsApp
            </button>
            ''',
            telefono,
            mensaje_encoded
        )
    enviar_whatsapp.short_description = "Invitación"

    class Media:
        js = ('admin/js/whatsapp_sender.js',)