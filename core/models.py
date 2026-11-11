from django.db import models
from django.utils import timezone

# Create your models here.


class SiteSettings(models.Model):
    """Model for website settings and configuration"""
    site_name = models.CharField(max_length=100, default='Medical Clinic')
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Doctor Information
    doctor_name = models.CharField(max_length=100)
    doctor_title = models.CharField(max_length=200)
    doctor_image = models.ImageField(upload_to='doctor/')
    doctor_biography = models.TextField()
    doctor_qualifications = models.TextField(help_text='Comma separated qualifications')
    doctor_experience = models.TextField()
    doctor_certifications = models.TextField(blank=True)
    doctor_achievements = models.TextField(blank=True)
    doctor_email = models.EmailField()
    doctor_phone = models.CharField(max_length=20)
    
    # Clinic Information
    clinic_name = models.CharField(max_length=100)
    clinic_address = models.TextField()
    clinic_phone = models.CharField(max_length=20)
    clinic_email = models.EmailField()
    working_hours = models.TextField()
    google_maps_embed = models.TextField(blank=True, help_text='Google Maps embed URL')
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Statistics
    years_experience = models.IntegerField(default=0)
    happy_patients = models.IntegerField(default=0)
    operations_completed = models.IntegerField(default=0)
    awards_won = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']