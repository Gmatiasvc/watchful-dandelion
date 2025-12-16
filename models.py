from django.db import models

class Asistencia(models.Model):
    # Mapeo exacto de la tabla 'data' de tu data.sqlite
    # id_hash VARCHAR(64) PRIMARY KEY
    id_hash = models.CharField(max_length=64, primary_key=True, verbose_name="Hash ID")
    
    # time_entry BIGINT NOT NULL
    time_entry = models.BigIntegerField(default=0, verbose_name="Hora de Entrada (Unix)")
    
    # time_exit BIGINT NOT NULL
    time_exit = models.BigIntegerField(default=0, verbose_name="Hora de Salida (Unix)")

    class Meta:
        # Esto le dice a Django que use la tabla 'data' existente
        db_table = 'data'
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"

    def __str__(self):
        return self.id_hash