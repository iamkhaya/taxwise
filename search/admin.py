from django.contrib import admin

from .models import Tarriff, Chapter

class TarriffAdmin(admin.ModelAdmin):
  list_display = ['chapter', 'description']

admin.site.register(Tarriff, TarriffAdmin)
admin.site.register(Chapter)
