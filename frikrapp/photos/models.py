#  -*- coding: utf-8 -*-
# lo de arriba es para las tildes
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
DEFAULT_LICENSES = (
    ('RIG','Copyright'),
    ('LEF','Copyleft'),
    ('CC','Creative Commons'),
)

LICENSES = getattr(settings, 'LICENSES', DEFAULT_LICENSES)

VISIBILITY_PUBLIC = 'PUB'
VISIBILITY_PRIVATE = 'PRI'

VISIBILITY = (
    (VISIBILITY_PUBLIC,'Publica'),
    (VISIBILITY_PRIVATE,'Privada')
)

# Permite que BADWORDS se pueda sobreescribir desde el settings.py
BADWORDS = getattr(settings, 'BADWORDS', ())


#Clase Photo que hereda de models.Model
# se hace para que rellene los campos de una tabla de fotos, pero que nosotros no gestionamos pero que es necesario

class Photo(models.Model):

    owner = models.ForeignKey(User)# Para meter el campo propietario
    name=models.CharField(max_length=150)#Siempre hay que poner una ruta maxima
    url = models.URLField()
    description = models.TextField(blank=True) #Con True se pone como que es opcional
    created_at= models.DateTimeField(auto_now_add=True)#Para saber en que momento se ha creado algo en la BBDD
    modified_at = models.DateTimeField(auto_now_add=True, auto_now=True)#Para saber en que momento se ha modificado algo en la BBDD
    license = models.CharField(max_length=3, choices=LICENSES)
    visibility= models.CharField(max_length=3, choices=VISIBILITY)#Para meter el campo visibilidad al modelo de la photo

    def __unicode__(self):
        return self.name
# Create your models here.

    def clean(self):
        for badword in BADWORDS:
            if badword in self.description:
                raise ValidationError(badword + u' no esta permitido')
