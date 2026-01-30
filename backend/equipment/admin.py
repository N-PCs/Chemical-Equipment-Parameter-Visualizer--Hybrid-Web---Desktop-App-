"""
Equipment App - Admin Configuration
"""
from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'id')
    readonly_fields = ('id', 'uploaded_at')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Dataset Information', {
            'fields': ('id', 'filename', 'uploaded_at')
        }),
        ('Summary Statistics', {
            'fields': ('total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution')
        }),
        ('Raw Data', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
    )
