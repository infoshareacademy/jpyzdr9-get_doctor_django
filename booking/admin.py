from django.contrib import admin
from .models import Appointment, Service

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'slot', 'created_at')
    list_filter = ('created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'price')  # поля, которые будут видны в списке
    list_filter = ('doctor',)
    search_fields = ('name', 'doctor__username')