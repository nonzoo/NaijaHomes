from django.contrib import admin
from .models import AgentProfile, CustomerProfile

admin.site.register(AgentProfile)
admin.site.register(CustomerProfile)