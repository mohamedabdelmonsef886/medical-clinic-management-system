from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from datetime import datetime, date, timedelta 
from django.utils import timezone
from django.conf import settings
from appointments.models import Appointment, ClinicAvailability, ClinicLocation
from appointments.forms import ClinicAvailabilityForm
from services.models import Service
from testimonials.models import Testimonial
from blog.models import BlogPost
from core.models import ContactMessage, SiteSettings
from .forms import SiteSettingsForm, ServiceForm, TestimonialForm, BlogPostForm
from appointments.sms import send_sms_notification, send_confirmation_email
# Try to import SMS functions, but don't fail if not available
try:
    from appointments.sms import send_sms_notification, send_confirmation_email
except ImportError:
    # Fallback functions if sms module is not available
    def send_sms_notification(appointment):
        print(f"SMS would be sent to {appointment.patient_phone}")
        return True
    
    def send_confirmation_email(appointment):
        print(f"Email would be sent to {appointment.patient_email}")
        return True

import os

# Dashboard Home
@login_required
def dashboard_home(request):
    """Dashboard home view with statistics"""
    today = date.today()
    
    context = {
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'total_services': Service.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
        'total_blog_posts': BlogPost.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/home.html', context)

# Appointment Management
@login_required
def appointment_list(request):
    """View all appointments with filtering"""
    # Add order_by to fix the pagination warning
    appointments = Appointment.objects.all().order_by('-appointment_date', '-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        appointments = appointments.filter(
            Q(patient_name__icontains=search) |
            Q(patient_email__icontains=search) |
            Q(patient_phone__icontains=search)
        )
    
    paginator = Paginator(appointments, 20)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    
    return render(request, 'dashboard/appointments/list.html', {
        'appointments': appointments,
        'status_choices': Appointment.STATUS_CHOICES,
        'current_status': status,
        'search': search,
    })

@login_required
def appointment_update_status(request, pk):
    """Update appointment status"""
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    return redirect('dashboard:appointments')

@login_required
def appointment_detail(request, pk):
    """View appointment details with ability to assign time and confirm"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        # Get form data
        new_status = request.POST.get('status')
        appointment_time = request.POST.get('appointment_time')
        notes = request.POST.get('notes', '')
        
        # Update fields
        if new_status:
            appointment.status = new_status
        
        if appointment_time:
            try:
                time_obj = datetime.strptime(appointment_time, '%H:%M').time()
                appointment.appointment_time = time_obj
            except ValueError:
                pass
        
        if notes:
            appointment.notes = notes
        
        appointment.save()
        
        # Send SMS notification (always)
        sms_sent = send_sms_notification(appointment)
        
        # Send Email only if email exists
        email_sent = False
        if appointment.patient_email:
            email_sent = send_confirmation_email(appointment)
        
        if new_status in ['confirmed', 'approved'] and appointment.appointment_time:
            if sms_sent:
                messages.success(request, '✅ Appointment confirmed! SMS sent to patient.')
                if email_sent:
                    messages.info(request, '📧 Email confirmation also sent to patient.')
            else:
                messages.warning(request, '⚠️ Appointment confirmed but SMS failed to send.')
        else:
            messages.success(request, '✅ Appointment updated successfully!')
        
        return redirect('dashboard:appointment_detail', pk=appointment.id)
    
    # Get available time slots for this date
    available_slots = []
    if appointment.appointment_date:
        # Check if there's availability for this date
        availabilities = ClinicAvailability.objects.filter(
            location=appointment.location,
            date=appointment.appointment_date,
            is_available=True
        )
        
        for availability in availabilities:
            # Generate slots for this availability
            current = datetime.combine(availability.date, availability.start_time)
            end = datetime.combine(availability.date, availability.end_time)
            
            while current < end:
                slot_end = current + timedelta(minutes=availability.slot_duration)
                # Check if this slot is already booked by another appointment
                is_booked = Appointment.objects.filter(
                    availability=availability,
                    appointment_time=current.time(),
                    status__in=['approved', 'confirmed', 'pending']
                ).exclude(id=appointment.id).exists()
                
                if not is_booked:
                    available_slots.append({
                        'time': current.time(),
                        'formatted': f"{current.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}"
                    })
                current = slot_end
    
    context = {
        'appointment': appointment,
        'available_slots': available_slots,
        'status_choices': Appointment.STATUS_CHOICES,
    }
    return render(request, 'dashboard/appointments/detail.html', context)

@login_required
def appointment_delete(request, pk):
    """Delete appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('dashboard:appointments')
    return render(request, 'dashboard/appointments/delete.html', {'appointment': appointment})

# Service Management
@login_required
def service_list(request):
    """View all services"""
    services = Service.objects.all()
    return render(request, 'dashboard/services/list.html', {'services': services})

@login_required
def service_create(request):
    """Create a new service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('dashboard:services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/services/form.html', {'form': form, 'title': 'Add Service', 'icon': 'plus'})

@login_required
def service_edit(request, pk):
    """Edit an existing service"""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('dashboard:services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'dashboard/services/form.html', {'form': form, 'service': service, 'title': 'Edit Service', 'icon': 'edit'})

@login_required
def service_delete(request, pk):
    """Delete a service"""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('dashboard:services')
    return render(request, 'dashboard/services/delete.html', {'service': service})

# Testimonial Management
@login_required
def testimonial_list(request):
    """View all testimonials"""
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials/list.html', {'testimonials': testimonials})

@login_required
def testimonial_create(request):
    """Create a new testimonial"""
    if request.method == 'POST':
        from .forms import TestimonialForm
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial created successfully!')
            return redirect('dashboard:testimonials')
    else:
        from .forms import TestimonialForm
        form = TestimonialForm()
    return render(request, 'dashboard/testimonials/form.html', {'form': form})

@login_required
def testimonial_edit(request, pk):
    """Edit an existing testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        from .forms import TestimonialForm
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('dashboard:testimonials')
    else:
        from .forms import TestimonialForm
        form = TestimonialForm(instance=testimonial)
    return render(request, 'dashboard/testimonials/form.html', {'form': form, 'testimonial': testimonial})

@login_required
def testimonial_delete(request, pk):
    """Delete a testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully!')
        return redirect('dashboard:testimonials')
    return render(request, 'dashboard/testimonials/delete.html', {'testimonial': testimonial})

# Blog Management
@login_required
def blog_list(request):
    """View all blog posts"""
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog/list.html', {'posts': posts})

@login_required
def blog_create(request):
    """Create a new blog post"""
    if request.method == 'POST':
        from .forms import BlogPostForm
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('dashboard:blog')
    else:
        from .forms import BlogPostForm
        form = BlogPostForm()
    return render(request, 'dashboard/blog/form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    """Edit an existing blog post"""
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        from .forms import BlogPostForm
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard:blog')
    else:
        from .forms import BlogPostForm
        form = BlogPostForm(instance=post)
    return render(request, 'dashboard/blog/form.html', {'form': form, 'post': post})

@login_required
def blog_delete(request, pk):
    """Delete a blog post"""
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('dashboard:blog')
    return render(request, 'dashboard/blog/delete.html', {'post': post})

# Contact Messages
@login_required
def contact_list(request):
    """View all contact messages"""
    messages_list = ContactMessage.objects.all()
    
    # Mark as read if requested
    if request.GET.get('mark_read'):
        msg = get_object_or_404(ContactMessage, pk=request.GET.get('mark_read'))
        msg.is_read = True
        msg.save()
    
    return render(request, 'dashboard/contacts/list.html', {'messages': messages_list})

@login_required
def contact_detail(request, pk):
    """View contact message detail"""
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    return render(request, 'dashboard/contacts/detail.html', {'message': message})

@login_required
def contact_delete(request, pk):
    """Delete contact message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('dashboard:contacts')
    return render(request, 'dashboard/contacts/delete.html', {'message': message})

# Settings
@login_required
def settings_edit(request):
    """Edit website settings with tabbed interface"""
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings()
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Settings updated successfully!')
            return redirect('dashboard:settings')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    
    context = {
        'form': form,
        'settings': settings_obj,
        'active_tab': request.GET.get('tab', 'general'),
    }
    return render(request, 'dashboard/settings/edit.html', context)

@login_required
def location_list(request):
    """View all clinic locations"""
    locations = ClinicLocation.objects.all().order_by('city', 'name')
    
    context = {
        'locations': locations,
    }
    return render(request, 'dashboard/locations/list.html', context)

@login_required
def location_add(request):
    """Add new clinic location"""
    if request.method == 'POST':
        # Manual form handling for location
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        is_active = request.POST.get('is_active') == 'on'
        
        if name and city and phone:
            location = ClinicLocation.objects.create(
                name=name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                phone=phone,
                email=email,
                is_active=is_active
            )
            messages.success(request, f'✅ Location "{location.name}" created successfully!')
            return redirect('dashboard:location_list')
        else:
            messages.error(request, '❌ Please fill in all required fields (Name, City, Phone)')
    
    return render(request, 'dashboard/locations/form.html', {'title': 'Add Location'})

@login_required
def location_edit(request, pk):
    """Edit clinic location"""
    location = get_object_or_404(ClinicLocation, pk=pk)
    
    if request.method == 'POST':
        location.name = request.POST.get('name', location.name)
        location.address = request.POST.get('address', location.address)
        location.city = request.POST.get('city', location.city)
        location.state = request.POST.get('state', location.state)
        location.zip_code = request.POST.get('zip_code', location.zip_code)
        location.phone = request.POST.get('phone', location.phone)
        location.email = request.POST.get('email', location.email)
        location.is_active = request.POST.get('is_active') == 'on'
        location.save()
        
        messages.success(request, f'✅ Location "{location.name}" updated successfully!')
        return redirect('dashboard:location_list')
    
    context = {
        'location': location,
        'title': 'Edit Location',
    }
    return render(request, 'dashboard/locations/form.html', context)

@login_required
def location_delete(request, pk):
    """Delete clinic location"""
    location = get_object_or_404(ClinicLocation, pk=pk)
    
    if request.method == 'POST':
        location_name = location.name
        location.delete()
        messages.success(request, f'✅ Location "{location_name}" deleted successfully!')
        return redirect('dashboard:location_list')
    
    context = {
        'location': location,
    }
    return render(request, 'dashboard/locations/delete.html', context)
@login_required
def availability_list(request):
    """View all clinic availability"""
    availabilities = ClinicAvailability.objects.all().order_by('date', 'location__name')
    
    # Filter by location
    location_id = request.GET.get('location')
    if location_id:
        availabilities = availabilities.filter(location_id=location_id)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        from datetime import datetime
        availabilities = availabilities.filter(date__gte=datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        from datetime import datetime
        availabilities = availabilities.filter(date__lte=datetime.strptime(date_to, '%Y-%m-%d').date())
    
    # Get locations for filter
    locations = ClinicLocation.objects.filter(is_active=True)
    
    context = {
        'availabilities': availabilities,
        'locations': locations,
        'selected_location': location_id,
    }
    return render(request, 'dashboard/availability/list.html', context)

@login_required
def availability_add(request):
    """Add new clinic availability"""
    if request.method == 'POST':
        form = ClinicAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save()
            messages.success(request, f'✅ Availability added for {availability.location.name} on {availability.date}')
            return redirect('dashboard:availability_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ClinicAvailabilityForm()
    
    context = {
        'form': form,
        'title': 'Add Availability',
    }
    return render(request, 'dashboard/availability/form.html', context)

@login_required
def availability_edit(request, pk):
    """Edit clinic availability"""
    availability = get_object_or_404(ClinicAvailability, pk=pk)
    
    if request.method == 'POST':
        form = ClinicAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Availability updated for {availability.location.name} on {availability.date}')
            return redirect('dashboard:availability_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ClinicAvailabilityForm(instance=availability)
    
    context = {
        'form': form,
        'availability': availability,
        'title': 'Edit Availability',
    }
    return render(request, 'dashboard/availability/form.html', context)

@login_required
def availability_delete(request, pk):
    """Delete clinic availability"""
    availability = get_object_or_404(ClinicAvailability, pk=pk)
    
    if request.method == 'POST':
        location_name = availability.location.name
        date_str = availability.date.strftime('%B %d, %Y')
        availability.delete()
        messages.success(request, f'✅ Availability for {location_name} on {date_str} deleted successfully!')
        return redirect('dashboard:availability_list')
    
    context = {
        'availability': availability,
    }
    return render(request, 'dashboard/availability/delete.html', context)

