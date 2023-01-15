from django.contrib import admin
from .models import *


@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'score']

