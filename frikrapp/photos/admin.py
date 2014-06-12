from django.contrib import admin
from models import Photo

class PhotoAdmin(admin.ModelAdmin):

    #Tunning del listado
    list_display = ('name','owner_name','license','visibility')
    list_filter = ('license','visibility')
    search_fields = ('name','description')

    def owner_name(self,obj):
        return obj.owner.first_name + ' ' + obj.owner.last_name

    owner_name.short_description = 'Propietario'
    owner_name.admin_order_field = 'owner'

    #Tunning del detalle
    fieldsets = (
        (
            None,
            {
                'fields': ('name',)
            }
        ),
        (
            'Descripcion y autor',
            {
                'fields': ('description','owner')
            }

        ),
        (
            'URL, licencia y visibilidad',
            {
                'classes': ('collapse',),
                'fields': ('url','license','visibility')
            }

        )
    )

admin.site.register(Photo, PhotoAdmin)

# Register your models here.
