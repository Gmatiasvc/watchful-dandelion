from django.db import models

class Asistencia(models.Model):
    # Mapeo de la tabla 'data'
    # id_hash VARCHAR(64) PRIMARY KEY
    id_hash = models.CharField(max_length=64, primary_key=True, verbose_name="Hash ID")
    
    # MEJORA: Persistencia de datos personales
    # Se agregan campos para almacenar la información legible para reportes.
    # blank=True, null=True permite compatibilidad con registros antiguos si los hubiera.
    nombre = models.CharField(max_length=100, verbose_name="Nombre", blank=True, null=True)
    apellido = models.CharField(max_length=100, verbose_name="Apellido", blank=True, null=True)
    documento = models.CharField(max_length=20, verbose_name="Documento", blank=True, null=True)
    
    # time_entry BIGINT NOT NULL
    time_entry = models.BigIntegerField(default=0, verbose_name="Hora de Entrada (Unix)")
    
    # time_exit BIGINT NOT NULL
    time_exit = models.BigIntegerField(default=0, verbose_name="Hora de Salida (Unix)")

    class Meta:
        # Esto le dice a Django que use la tabla 'data'
        db_table = 'data'
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"

    def __str__(self):
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido} ({self.id_hash[:8]}...)"
        return self.id_hash