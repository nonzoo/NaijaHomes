from django.contrib import admin
from .models import Properties,Favorite


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "address", "is_featured")
    list_editable = ("is_featured",)


admin.site.register(Favorite)