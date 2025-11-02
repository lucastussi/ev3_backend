from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'criticality', 'status', 'owner', 'created_at')
    list_filter = ('criticality', 'status', 'category')
    search_fields = ('name', 'category', 'owner__username')
    ordering = ('-created_at',)