from .models import SiteSettings
from services.models import Service
from blog.models import BlogPost
from appointments.models import Appointment
from django.utils.translation import get_language

def site_settings(request):
    """Add site settings and global data to all templates"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    # Get active services
    services = Service.objects.filter(is_active=True)[:6] if settings else []
    
    # Get latest blog posts
    latest_posts = BlogPost.objects.filter(is_published=True)[:3] if settings else []
    
    # Get pending appointments count for badge
    pending_count = 0
    try:
        pending_count = Appointment.objects.filter(status='pending').count()
    except:
        pass

    return {
        'site_settings': settings,
        'services_global': services,
        'latest_posts_global': latest_posts,
        'pending_appointments_count': pending_count,
        'current_language': get_language(),  # Add current language
    }