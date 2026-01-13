from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime
import pytz
from django.conf import settings
from .models import Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista
    list_display = ('get_nombre_completo', 'get_documento', 'get_hora_entrada', 'get_hora_salida', 'get_duracion')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'apellido', 'documento', 'id_hash')
    
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