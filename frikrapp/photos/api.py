# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from serializers import UserSerializer, PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from models import Photo
from models import VISIBILITY_PUBLIC
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from permissions import UserPermission
from django.db.models import Q

class UserListAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request):
        users = User.objects.all() # Con esto recuperamos todos los usuarios de la api
        serializer = UserSerializer(users, many=True) # con el many a true significa que se le pasan muchos usuarios
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class UserDetailAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=202)
            else:
                return Response(serializer.errors,status=400)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request,pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoAPIQueryset:
    def get_queryset(self):
        """
        Devuelve un queryset en funcion
        """
        if self.request.user.is_superuser:
            return Photo.objects.all()
        elif self.request.user.is_authenticated():
            return Photo.objects.filter(Q(visibility=VISIBILITY_PUBLIC)|Q(owner=self.request.user))
        else:
            return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)

class PhotoListApi(APIView):

    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data,status=202)


class PhotoListApi(PhotoAPIQueryset,ListCreateAPIView):
    """
    Implementa el API de listado (GET) y creacion (POST) de fotos
    (Si, en serio)
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Devuelve un queryset en funcion
        """
        if self.request.user.is_superuser:
            return Photo.objects.all()
        elif self.request.user.is_authenticated():
            return Photo.objects.filter(Q(visibility=VISIBILITY_PUBLIC)|Q(owner=self.request.user))
        else:
            return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)

    def get_serializer_class(self):
    #    return self.serializer_class
        return PhotoSerializer if self.request.method == "POST" else self.serializer_class

    def pre_save(self, obj):
        """
        Asigna la autoria de la foto al usuario autenticado al crearla
        """
        obj.owner = self.request.user

class PhotoDetailAPI(PhotoAPIQueryset, RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
