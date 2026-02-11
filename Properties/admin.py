from django.contrib import admin
from .models import Properties,Favorite,PropertyImage


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "address", "is_featured")
    list_editable = ("is_featured",)
    search_fields = ['title','address']

admin.site.register(PropertyImage)
admin.site.register(Favorite)