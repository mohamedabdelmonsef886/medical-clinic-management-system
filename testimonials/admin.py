from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'rating', 'is_featured', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_approved']
    search_fields = ['patient_name', 'review']
    ordering = ['-created_at']