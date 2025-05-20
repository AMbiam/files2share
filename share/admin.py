from django.contrib import admin

from . import models
# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'title',)

class AccessAdmin(admin.ModelAdmin):
    list_display = ('fileobj',)

#Model is attached to the admin model.
admin.site.register(models.File, FileAdmin)
admin.site.register(models.Access, AccessAdmin)