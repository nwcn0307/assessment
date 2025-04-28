from django.contrib import admin
from .models import Resource
# Register your models here.
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'description', 'website')
    list_display_links = ('id', 'name')
    #search_fields = ('name')
    list_per_page =25

admin.site.register(Resource, ResourceAdmin)