from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('success/', views.appointment_success, name='success'),
    
    # API endpoints
    path('api/available-dates/', views.get_available_dates, name='api_available_dates'),
    path('api/available-slots/', views.get_available_slots, name='api_available_slots'),
    path('api/send-sms/<int:appointment_id>/', views.send_sms_api, name='api_send_sms'),
    path('api/send-email/<int:appointment_id>/', views.send_email_api, name='api_send_email'),
]