from django.contrib import admin
from .models import AgentProfile, CustomerProfile, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        'phone_number',
        "is_staff",
        "is_active",
        "get_groups",
        "last_login",
    )

    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    
    # ✅ SHOW phone_number on the "Change user" page
    fieldsets = UserAdmin.fieldsets + (
        (_("Extra info"), {"fields": ("phone_number",)}),
    )

    # ✅ SHOW phone_number on the "Add user" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Extra info"), {"fields": ("phone_number",)}),
    )
    
    def get_groups(self, obj):
        return ", ".join(obj.groups.values_list("name", flat=True))

    get_groups.short_description = "Groups"

admin.site.register(AgentProfile)
admin.site.register(CustomerProfile)