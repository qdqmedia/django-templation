from __future__ import absolute_import
from django.contrib import admin
from .settings import get_resource_access_model


class ResourceAccessAdmin(admin.ModelAdmin):
    fields = ('user', 'resource', 'is_validated', 'access_token')
    list_display = ('user', 'resource', 'is_validated')
    raw_id_fields = ('user', 'resource')
    readonly_fields = ('access_token',)

    def access_token(self, obj):
        return obj.get_access_token()

admin.site.register(get_resource_access_model(), ResourceAccessAdmin)
