from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Servicio(models.Model):
    descripcion=models.TextField(null=True)
    tipo=models.CharField(max_length=20)
    duracion=models.DurationField()
    precio=models.FloatField()
    activo=models.BooleanField()


class Cita(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE='pendiente_abono','Pendiente de Abono'
        CONFIRMADA='confirmada','Confirmada'
        COMPLETADA='completada','Completada'
        CANCELADA='cancelada','Cancelada'
    #vinculado a cliente,inicio,final,estado,total,notas
    imagen_referencia=models.ImageField(null=True,upload_to="users/imagen_referencias")
    user=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='citas',null=True)
    servicio=models.ForeignKey(Servicio,on_delete=models.SET_NULL,related_name='citas',null=True)
    inicio=models.DateTimeField(auto_now=False, auto_now_add=False)
    final=models.DateTimeField(auto_now=False, auto_now_add=False)
    estado=models.CharField(max_length=20,choices=Estado,default=Estado.PENDIENTE)

    total_usd=models.DecimalField(max_digits=8,decimal_places=2)
    referencia=models.CharField(max_length=60,blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    

class Horario(models.Model):
    dia_semana=models.PositiveSmallIntegerField()
    hora_inicio=models.TimeField()
    hora_fin=models.TimeField()


#EN ESTA PARTE DEJO NOTAS, DE CAMBIOS QUE LE PUEDO HACER LA BD DESPUES

#Capaz una tabla de pagos?

#una clase de extras servicios tambien puede ser


#tabla descartada por ahora
"""class Cliente(models.Model):
    user=models.OneToOneField("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    notas=models.TextField()
    creado_en=models.DateTimeField(auto_now_add=True)

    pass
"""
