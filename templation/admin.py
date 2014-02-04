from django.contrib import admin
from .settings import get_resource_access_model


class ResourceAccessAdmin(admin.ModelAdmin):
    fields = ('user', 'resource', 'is_validated')
    list_display = ('user', 'resource', 'is_validated')

admin.site.register(get_resource_access_model(), ResourceAccessAdmin)
