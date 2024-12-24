from django.contrib import admin
from .models import Cow, MilkProduction, VeterinaryRecord

#admin.site.register(Cow)
#admin.site.register(MilkProduction)
#admin.site.register(VeterinaryRecord)

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'name', 'breed', 'status', 'current_lactation')
    list_filter = ('status', 'breed')
    search_fields = ('tag_number', 'name')
    ordering = ('tag_number',)

@admin.register(MilkProduction)
class MilkProductionAdmin(admin.ModelAdmin):
    list_display = ('cow', 'date', 'morning_amount', 'evening_amount', 'total_production')
    list_filter = ('date', 'cow')
    date_hierarchy = 'date'

@admin.register(VeterinaryRecord)
class VeterinaryRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'date', 'record_type', 'veterinarian')
    list_filter = ('record_type', 'date', 'veterinarian')
    search_fields = ('cow__tag_number', 'diagnosis', 'treatment')
