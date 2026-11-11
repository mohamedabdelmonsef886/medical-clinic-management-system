from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, ClinicLocation, ClinicAvailability
from .forms import AppointmentBookingForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .sms import send_sms_notification, send_confirmation_email
def get_available_dates(request):
    """AJAX endpoint to get available dates for a location"""
    location_id = request.GET.get('location_id')
    if not location_id:
        return JsonResponse({'error': 'Location ID required'}, status=400)
    
    try:
        location = ClinicLocation.objects.get(id=location_id)
        
        # Get available dates from ClinicAvailability
        availabilities = ClinicAvailability.objects.filter(
            location=location,
            is_available=True,
            date__gte=timezone.now().date()
        ).order_by('date')
        
        available_dates = []
        for availability in availabilities:
            # Check if there are any available time slots for this date
            from datetime import datetime, timedelta
            slots = []
            current = datetime.combine(availability.date, availability.start_time)
            end = datetime.combine(availability.date, availability.end_time)
            
            while current < end:
                slot_end = current + timedelta(minutes=availability.slot_duration)
                # Check if this slot is already booked
                is_booked = Appointment.objects.filter(
                    availability=availability,
                    appointment_time=current.time(),
                    status__in=['approved', 'confirmed', 'pending']
                ).exists()
                
                if not is_booked:
                    slots.append({
                        'start': current.time(),
                        'end': slot_end.time(),
                    })
                current = slot_end
            
            # Only show dates that have available slots
            if slots:
                available_dates.append({
                    'date': availability.date.isoformat(),
                    'day': availability.date.strftime('%A'),
                    'formatted': availability.date.strftime('%B %d, %Y'),
                    'available_slots': len(slots),
                    'availability_id': availability.id,
                })
        
        return JsonResponse({'dates': available_dates})
    except ClinicLocation.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def get_available_slots(request):
    """AJAX endpoint to get available time slots for a specific date and location"""
    availability_id = request.GET.get('availability_id')
    if not availability_id:
        return JsonResponse({'error': 'Availability ID required'}, status=400)
    
    try:
        availability = ClinicAvailability.objects.get(id=availability_id)
        
        # Generate time slots for this availability
        from datetime import datetime, timedelta
        slots = []
        current = datetime.combine(availability.date, availability.start_time)
        end = datetime.combine(availability.date, availability.end_time)
        
        while current < end:
            slot_end = current + timedelta(minutes=availability.slot_duration)
            
            # Check if this slot is already booked
            is_booked = Appointment.objects.filter(
                availability=availability,
                appointment_time=current.time(),
                status__in=['approved', 'confirmed', 'pending']
            ).exists()
            
            if not is_booked:
                slots.append({
                    'start': current.time(),
                    'end': slot_end.time(),
                    'time': current.strftime('%H:%M'),
                    'formatted': f"{current.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}"
                })
            
            current = slot_end
        
        return JsonResponse({
            'slots': slots,
            'date': availability.date.isoformat(),
            'location': availability.location.name
        })
    except ClinicAvailability.DoesNotExist:
        return JsonResponse({'error': 'Availability not found'}, status=404)

def book_appointment(request):
    """View for booking an appointment - without time slot selection"""
    
    # Get all active locations
    locations = ClinicLocation.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Debug: Print all POST data
        print("=" * 60)
        print("📝 BOOKING POST DATA:")
        for key, value in request.POST.items():
            print(f"  {key}: {value}")
        print("=" * 60)
        
        # Get form data directly from POST
        patient_name = request.POST.get('patient_name', '').strip()
        patient_phone = request.POST.get('patient_phone', '').strip()
        patient_email = request.POST.get('patient_email', '').strip()
        patient_age = request.POST.get('patient_age', '')
        reason_for_visit = request.POST.get('reason_for_visit', '').strip()
        notes = request.POST.get('notes', '').strip()
        location_id = request.POST.get('location', '').strip()
        appointment_date_str = request.POST.get('appointment_date', '').strip()
        
        print(f"📍 Location ID from POST: '{location_id}'")
        print(f"📅 Date from POST: '{appointment_date_str}'")
        
        # Validate required fields
        errors = []
        if not patient_name:
            errors.append('Patient name is required')
        if not patient_phone:
            errors.append('Phone number is required')
        if not patient_email:
            errors.append('Email is required')
        if not reason_for_visit:
            errors.append('Reason for visit is required')
        if not location_id:
            errors.append('Location is required')
        if not appointment_date_str:
            errors.append('Appointment date is required')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'appointments/book_appointment.html', {
                'locations': locations,
            })
        
        try:
            # Get the location
            location = ClinicLocation.objects.get(id=location_id)
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
            
            # Create the appointment (without time - will be assigned by clinic)
            appointment = Appointment.objects.create(
                patient_name=patient_name,
                patient_phone=patient_phone,
                patient_email=patient_email,
                patient_age=int(patient_age) if patient_age else None,
                location=location,
                appointment_date=appointment_date,
                appointment_time=None,  # Time will be assigned by clinic
                reason_for_visit=reason_for_visit,
                notes=notes,
                status='pending'
            )
            
            print(f"✅ Appointment created! ID: {appointment.id}")
            print(f"📍 Location: {appointment.location.name}")
            print(f"📅 Date: {appointment.appointment_date}")
            print(f"🕐 Time: To be assigned by clinic")
            
            # Send booking confirmation
            try:
                send_booking_confirmation(appointment)
            except Exception as e:
                print(f"Notification error: {e}")
            
            messages.success(
                request, 
                '✅ Your appointment request has been submitted successfully! '
                'The clinic will confirm your appointment and send you the exact time via SMS/email.'
            )
            return redirect('appointments:success')
            
        except ClinicLocation.DoesNotExist:
            print(f"❌ Location with ID {location_id} not found")
            messages.error(request, 'Selected location does not exist.')
        except ValueError as e:
            print(f"❌ Date parsing error: {e}")
            messages.error(request, f'Invalid date format: {str(e)}')
        except Exception as e:
            print(f"❌ Error creating appointment: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'An error occurred: {str(e)}')
        
        return render(request, 'appointments/book_appointment.html', {
            'locations': locations,
        })
    
    # GET request
    context = {
        'locations': locations,
    }
    return render(request, 'appointments/book_appointment.html', context)
def send_booking_confirmation(appointment):
    """Send booking confirmation to patient (without time)"""
    details = appointment.get_appointment_details()
    
    message = f"""
🏥 Appointment Request Received

Dear {details['patient']},

Your appointment request has been received!

📍 Location: {details['location']}
📅 Date: {details['date']}
🕐 Time: To be confirmed

We will review your request and send you the exact appointment time via SMS/email.

Thank you for choosing our clinic!
"""
    
    # Send SMS
    print("=" * 60)
    print("📱 SMS NOTIFICATION (Booking Request)")
    print("=" * 60)
    print(f"To: {appointment.patient_phone}")
    print(f"Message: {message}")
    print("=" * 60)
    
    # Send Email
    subject = f"Appointment Request Received - {getattr(settings, 'SITE_NAME', 'Medical Clinic')}"
    email_message = f"""
Dear {details['patient']},

Thank you for booking an appointment with us!

Your appointment request details:
----------------------------------
📍 Location: {details['location']}
📅 Date: {details['date']}
🕐 Time: To be confirmed
📊 Status: Pending
----------------------------------

We will review your request and send you the exact appointment time via SMS/email.

If you need to cancel or reschedule, please contact us.

Thank you for choosing our clinic!
"""
    
    try:
        send_mail(
            subject=subject,
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient_email],
            fail_silently=True,
        )
        print(f"✅ Email sent to {appointment.patient_email}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
def appointment_success(request):
    """View for appointment success page"""
    return render(request, 'appointments/appointment_success.html')

def send_sms_notification(appointment):
    """Send SMS notification to patient"""
    details = appointment.get_appointment_details()
    
    message = f"""
    🏥 Appointment Request Received
    
    Dear {details['patient']},
    
    Your appointment request has been received!
    
    📍 Location: {details['location']}
    📅 Date: {details['date']}
    🕐 Time: {details['time']}
    
    Status: {details['status']}
    
    We will confirm your appointment shortly.
    
    Thank you for choosing our clinic!
    """
    
    # For development, print to console
    print("=" * 60)
    print("SMS NOTIFICATION")
    print("=" * 60)
    print(f"To: {appointment.patient_phone}")
    print(f"Message: {message}")
    print("=" * 60)
    return True

def send_confirmation_email(appointment):
    """Send confirmation email to patient"""
    details = appointment.get_appointment_details()
    
    subject = f"Appointment Request - {getattr(settings, 'SITE_NAME', 'Medical Clinic')}"
    message = f"""
    Dear {details['patient']},
    
    Thank you for booking an appointment with us!
    
    Your appointment details:
    -------------------------
    📍 Location: {details['location']}
    📅 Date: {details['date']}
    🕐 Time: {details['time']}
    📊 Status: {details['status']}
    -------------------------
    
    We will confirm your appointment shortly.
    
    If you need to cancel or reschedule, please contact us.
    
    Thank you for choosing our clinic!
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient_email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
    

@csrf_exempt
@login_required
def send_sms_api(request, appointment_id):
    """API endpoint to send SMS notification"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        success = send_sms_notification(appointment)
        return JsonResponse({'success': success})
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@login_required
def send_email_api(request, appointment_id):
    """API endpoint to send email notification"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        success = send_confirmation_email(appointment)
        return JsonResponse({'success': success})
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)