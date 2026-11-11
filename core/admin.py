from django.contrib import admin
from .models import SiteSettings, ContactMessage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'doctor_name', 'clinic_name']
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_logo', 'site_favicon')
        }),
        ('Doctor Information', {
            'fields': ('doctor_name', 'doctor_title', 'doctor_image', 'doctor_biography', 
                        'doctor_qualifications', 'doctor_experience', 'doctor_certifications',
                        'doctor_achievements', 'doctor_email', 'doctor_phone')
        }),
        ('Clinic Information', {
            'fields': ('clinic_name', 'clinic_address', 'clinic_phone', 'clinic_email',
                        'working_hours', 'google_maps_embed')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')
        }),
        ('Statistics', {
            'fields': ('years_experience', 'happy_patients', 'operations_completed', 'awards_won')
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']