from django.contrib import admin
from .models import ResourceAccess


class ResourceAccessAdmin(admin.ModelAdmin):
    fields = ('user', 'resource')
    list_display = ('user', 'resource')

admin.site.register(ResourceAccess, ResourceAccessAdmin)
