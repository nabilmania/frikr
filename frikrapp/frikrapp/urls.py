#  -*- coding: utf-8 -*-
# lo de arriba es para las tildes
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from photos import views, api

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    #WEB URLS
    url(r'^$',views.HomeView.as_view()), #URL vacia para que al poner el 127.0.0.1 esta sea la pagina index
    url(r'^photos/$',views.PhotoListView.as_view()),
    # URL que lo que hace es coger todo el nombre que viene detras de photos lo mete en una variable
    # pk y todo esto es para numerar las photos que se le pasen
    url(r'^photos/(?P<pk>[0-9]+)$',views.PhotoDetailView.as_view()),
    # Para crearnos el login y logout, la vista del perfil, la de crear foto
    url(r'^login$',views.UserLoginView.as_view()),
    url(r'^logout$',views.UserLogoutView.as_view()),
    url(r'^profile$',views.UserProfileView.as_view()),
    url(r'^create$','photos.views.create_photo'),

    # User API URLs
    url(r'^api/1.0/users/$', api.UserListAPI.as_view()),
    url(r'^api/1.0/users/(?P<pk>[0-9]+)$', api.UserDetailAPI.as_view()),

    # User API URLs
    url(r'^api/1.0/photos/$', api.PhotoListApi.as_view()),
    url(r'^api/1.0/photos/(?P<pk>[0-9]+)$', api.PhotoDetailAPI.as_view())

)
