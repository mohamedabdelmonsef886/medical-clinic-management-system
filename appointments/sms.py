import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_sms_notification(appointment):
    """Send SMS notification to patient with appointment details"""
    details = appointment.get_appointment_details()
    
    # Format phone number (remove spaces, dashes, etc.)
    phone = appointment.patient_phone.strip()
    
    # Build SMS message
    message = f"""
🏥 Appointment Confirmation

Dear {details['patient']},

Your appointment has been confirmed!

📍 Location: {details['location']}
📅 Date: {details['date']}
🕐 Time: {details['time']}
📍 Address: {details['address']}

📞 Contact: {appointment.location.phone if appointment.location else 'N/A'}

Please arrive 15 minutes before your appointment.
Bring your ID and insurance card.

Thank you for choosing our clinic!
"""
    
    print("=" * 70)
    print("📱 SMS NOTIFICATION")
    print("=" * 70)
    print(f"To: {phone}")
    print(f"Subject: Appointment Confirmation")
    print(f"Message:\n{message}")
    print("=" * 70)
    
    # If Twilio is configured, send actual SMS
    if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            print("✅ SMS sent via Twilio")
            return True
        except Exception as e:
            print(f"❌ Twilio SMS error: {e}")
            return False
    
    # If SMS Gateway is configured
    elif hasattr(settings, 'SMS_GATEWAY_URL') and settings.SMS_GATEWAY_URL:
        try:
            payload = {
                'to': phone,
                'message': message,
                'api_key': settings.SMS_API_KEY
            }
            response = requests.post(settings.SMS_GATEWAY_URL, data=payload, timeout=10)
            if response.status_code == 200:
                print("✅ SMS sent via Gateway")
                return True
            else:
                print(f"❌ SMS Gateway error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ SMS Gateway error: {e}")
            return False
    
    # For development, just print
    print("ℹ️ SMS sent to console (development mode)")
    return True

def send_confirmation_email(appointment):
    """Send confirmation email to patient with appointment details"""
    details = appointment.get_appointment_details()
    
    subject = f"Appointment Confirmation - {getattr(settings, 'SITE_NAME', 'Medical Clinic')}"
    
    # HTML Email Template
    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #0056b3; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background: #f8f9fa; }}
        .details {{ background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .detail-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .footer {{ text-align: center; padding: 20px; color: #6c757d; font-size: 0.9rem; }}
        .badge {{ display: inline-block; padding: 3px 10px; background: #28a745; color: white; border-radius: 20px; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🏥 Appointment Confirmation</h2>
        </div>
        <div class="content">
            <p>Dear <strong>{details['patient']}</strong>,</p>
            <p>Your appointment has been <span class="badge">Confirmed</span></p>
            
            <div class="details">
                <h4>Appointment Details:</h4>
                <div class="detail-item"><strong>📍 Location:</strong> {details['location']}</div>
                <div class="detail-item"><strong>📅 Date:</strong> {details['date']}</div>
                <div class="detail-item"><strong>🕐 Time:</strong> {details['time']}</div>
                <div class="detail-item"><strong>📍 Address:</strong> {details['address']}</div>
                <div class="detail-item"><strong>📞 Contact:</strong> {appointment.location.phone if appointment.location else 'N/A'}</div>
            </div>
            
            <p><strong>Please arrive 15 minutes before your appointment.</strong></p>
            <p>Please bring:</p>
            <ul>
                <li>Your ID</li>
                <li>Insurance card (if applicable)</li>
                <li>List of current medications</li>
            </ul>
            
            <p>If you need to cancel or reschedule, please contact us at least 24 hours in advance.</p>
            
            <p>Thank you for choosing our clinic!</p>
            <p>Best regards,<br>
            <strong>{settings.SITE_NAME}</strong></p>
        </div>
        <div class="footer">
            <p>© {settings.SITE_NAME} - All rights reserved.</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Plain text version
    plain_message = f"""
Dear {details['patient']},

Your appointment has been confirmed!

Appointment Details:
-------------------
📍 Location: {details['location']}
📅 Date: {details['date']}
🕐 Time: {details['time']}
📍 Address: {details['address']}
📞 Contact: {appointment.location.phone if appointment.location else 'N/A'}
-------------------

Please arrive 15 minutes before your appointment.
Bring your ID and insurance card.

If you need to cancel or reschedule, please contact us at least 24 hours in advance.

Thank you for choosing our clinic!

Best regards,
{settings.SITE_NAME}
"""
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient_email],
            fail_silently=True,
        )
        print(f"✅ Email sent to {appointment.patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def send_booking_confirmation(appointment):
    """Send booking confirmation to patient (when first booked)"""
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
    
    print("=" * 70)
    print("📱 BOOKING CONFIRMATION SMS")
    print("=" * 70)
    print(f"To: {appointment.patient_phone}")
    print(f"Message:\n{message}")
    print("=" * 70)
    
    # Send email
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
        print(f"✅ Booking confirmation email sent to {appointment.patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False