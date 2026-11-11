from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_phone', 'patient_email', 'appointment_date', 
                   'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['patient_name', 'patient_phone', 'patient_email']
    ordering = ['-appointment_date', 'appointment_time']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_appointments', 'reject_appointments', 'complete_appointments']
    
    def approve_appointments(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} appointments approved.")
    approve_appointments.short_description = "Approve selected appointments"
    
    def reject_appointments(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} appointments rejected.")
    reject_appointments.short_description = "Reject selected appointments"
    
    def complete_appointments(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} appointments marked as completed.")
    complete_appointments.short_description = "Mark selected as completed"