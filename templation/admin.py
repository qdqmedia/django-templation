from __future__ import absolute_import
from django.contrib import admin
from .settings import get_resource_access_model


class ResourceAccessAdmin(admin.ModelAdmin):
    fields = ('user', 'resource_pointer', 'access_token')
    list_display = ('user', 'resource', 'is_validated')
    raw_id_fields = ('user', 'resource_pointer')
    readonly_fields = ('access_token',)

    def resource(self, obj):
        return obj.resource_pointer.resource

    def is_validated(self, obj):
        return obj.resource_pointer.is_validated

    def access_token(self, obj):
        return obj.get_access_token()

admin.site.register(get_resource_access_model(), ResourceAccessAdmin)
