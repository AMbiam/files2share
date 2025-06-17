from django.contrib import admin

# from . import models

from share.models.file import File
from share.models.access import Access

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'title',)

class AccessAdmin(admin.ModelAdmin):
    list_display = ('fileobj',)

#Model is attached to the admin model.
admin.site.register(File, FileAdmin)
admin.site.register(Access, AccessAdmin)