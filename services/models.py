from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('gynecology', 'Gynecology'),
        ('neurology', 'Neurology'),
        ('ophthalmology', 'Ophthalmology'),
        ('dentistry', 'Dentistry'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=50, default='fa-heartbeat')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., 30 minutes")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']