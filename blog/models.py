from django.db import models
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.
class BlogPost(models.Model):
    """Model for blog articles"""
    CATEGORY_CHOICES = [
        ('health_tips', 'Health Tips'),
        ('medical_updates', 'Medical Updates'),
        ('patient_stories', 'Patient Stories'),
        ('clinic_news', 'Clinic News'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Dr. Admin')
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title