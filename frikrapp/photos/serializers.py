# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings

class UserSerializer(serializers.Serializer):
    id= serializers.Field() #solo lectura
    first_name= serializers.CharField()
    last_name= serializers.CharField()
    username= serializers.CharField()
    email= serializers.CharField()
    password = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        """
        Devuelve un objeto User en funcion de attrs
        :param: attrs: diccionario con datos
        :param: instance: objeto user a actualizar
        :return: objeto User
        """
        if not instance:
            instance = User()

        instance.first_name = attrs.get('first_name')
        instance.last_name = attrs.get('last_name')
        instance.username = attrs.get('username')
        instance.email = attrs.get('email')
        #encriptamos password antes de asignar
        new_password = make_password(attrs.get('password'))
        instance.password=new_password

        return instance

    def validate(self, attrs):
        existent_users = User.objects.filter(username=attrs.get('username'))
        if len(existent_users)>0:
            raise serializers.ValidationError(u"Ya existe ese usuario")
        return attrs # todo ha ido ok

# Permite que BADWORDS se pueda sobreescribir desde el settings.py
BADWORDS = getattr(settings, 'BADWORDS', ())

# Las importaciones no tienen por qué ser el comienzo del fichero
from models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        read_only_fields = ('owner',)
"""
    def validate_description(self,attrs,source):
        description = attrs.get(source)
        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise serializers.ValidationError(badword + u" no esta permitido")
        return attrs # todo ha ido ok
"""


class PhotoListSerializer(PhotoSerializer):
    class Meta(PhotoSerializer.Meta):
        fields = ('id','owner','name')