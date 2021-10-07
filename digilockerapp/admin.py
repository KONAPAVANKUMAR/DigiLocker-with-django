from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(DocumentModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ("title","file")