from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import SiteSettings, ContactMessage
from services.models import Service
from testimonials.models import Testimonial
from blog.models import BlogPost
from appointments.forms import AppointmentBookingForm  
from appointments.models import Appointment

# Create your views here.
def home(request):
    """Home page view"""
    # Get site settings
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    # Get featured services
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    
    # Get featured testimonials
    testimonials = Testimonial.objects.filter(is_featured=True, is_approved=True)[:5]
    
    # Get latest blog posts
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Get statistics
    stats = {
        'years_experience': settings.years_experience if settings else 0,
        'happy_patients': settings.happy_patients if settings else 0,
        'operations_completed': settings.operations_completed if settings else 0,
        'awards_won': settings.awards_won if settings else 0,
    }
    
    # Appointment form
    form = AppointmentBookingForm()
    
    context = {
        'settings': settings,
        'featured_services': featured_services,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'stats': stats,
        'form': form,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    context = {
        'settings': settings,
    }
    
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save contact message
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Send email notification (optional)
        try:
            send_mail(
                subject=f"New Contact Message: {subject}",
                message=f"""
                Name: {name}
                Email: {email}
                Phone: {phone}
                Subject: {subject}
                Message: {message}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('core:contact')
    
    context = {
        'settings': settings,
    }
    
    return render(request, 'core/contact.html', context)