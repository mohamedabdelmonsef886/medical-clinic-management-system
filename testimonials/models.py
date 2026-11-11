from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Testimonial(models.Model):
    """Model for patient testimonials"""
    patient_name = models.CharField(max_length=100)
    patient_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    patient_condition = models.CharField(max_length=200, blank=True, help_text='e.g., Dental Patient, Orthopedic Patient')
    review = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.rating}/5"
    
    class Meta:
        ordering = ['-created_at']