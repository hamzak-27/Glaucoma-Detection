from django.contrib import admin
from .models import Patient, GlaucomaTest

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_created', 'test_count')
    search_fields = ('name', 'email')
    list_filter = ('date_created',)
    
    def test_count(self, obj):
        return obj.tests.count()
    test_count.short_description = 'Number of Tests'

@admin.register(GlaucomaTest)
class GlaucomaTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'status', 'is_glaucoma', 'confidence_percent', 'date_created', 'date_processed')
    list_filter = ('status', 'is_glaucoma', 'date_created')
    search_fields = ('patient__name', 'patient__email')
    readonly_fields = ('date_created', 'date_processed', 'processing_time', 'status')
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Test Data', {
            'fields': ('image', 'result_image')
        }),
        ('Results', {
            'fields': ('is_glaucoma', 'raw_score', 'confidence_score')
        }),
        ('Status', {
            'fields': ('status', 'error_message', 'date_created', 'date_processed', 'processing_time')
        }),
    )