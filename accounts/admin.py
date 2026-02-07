from django.contrib import admin
from .models import AgentProfile, CustomerProfile, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "get_groups",
        "last_login",
    )

    search_fields = ("username", "email")
    ordering = ("-date_joined",)


    
    def get_groups(self, obj):
        return ", ".join(obj.groups.values_list("name", flat=True))

    get_groups.short_description = "Groups"

admin.site.register(AgentProfile)
admin.site.register(CustomerProfile)