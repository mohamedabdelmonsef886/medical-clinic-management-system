from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, ClinicLocation, ClinicSchedule, TimeSlot, ClinicAvailability

class AppointmentBookingForm(forms.Form):
    """Form for booking appointments with location and date selection"""
    
    patient_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    patient_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'})
    )
    patient_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    patient_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    reason_for_visit = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Please describe your symptoms or reason for visit'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional information'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get available locations
        locations = ClinicLocation.objects.filter(is_active=True)
        location_choices = [(loc.id, f"{loc.name} - {loc.city}") for loc in locations]
        self.fields['location'] = forms.ChoiceField(
            choices=[('', 'Select a Location')] + location_choices,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'location-select'})
        )
        
        # Date selection - only allow future dates
        today = timezone.now().date()
        self.fields['appointment_date'] = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'id': 'date-select',
                'min': today.isoformat()
            })
        )

class ClinicAvailabilityForm(forms.ModelForm):
    """Form for clinic admin to add availability"""
    class Meta:
        model = ClinicAvailability
        fields = ['location', 'date', 'start_time', 'end_time', 'slot_duration', 'max_patients', 'is_available', 'notes']
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'slot_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'step': 15}),
            'max_patients': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class AppointmentTimeSelectionForm(forms.Form):
    """Form for selecting available time slots"""
    time_slot = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id', None)
        date = kwargs.pop('date', None)
        super().__init__(*args, **kwargs)
        
        if location_id and date:
            # Get available time slots for this location and date
            from .models import TimeSlot
            slots = TimeSlot.objects.filter(
                schedule__location_id=location_id,
                date=date,
                is_booked=False,
                is_available=True
            ).order_by('start_time')
            
            choices = [(slot.id, f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}") 
                        for slot in slots]
            self.fields['time_slot'].choices = [('', 'Select a time slot')] + choices

class AppointmentStatusForm(forms.ModelForm):
    """Form for updating appointment status and assigning time"""
    class Meta:
        model = Appointment
        fields = ['status', 'appointment_time', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Add this for backward compatibility
class AppointmentForm(forms.ModelForm):
    """Original Appointment Form for backward compatibility"""
    class Meta:
        model = Appointment
        fields = [
            'patient_name', 'patient_phone', 'patient_email', 
            'patient_age', 'appointment_date', 'appointment_time',
            'reason_for_visit', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason_for_visit': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time:
            if Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exists():
                raise forms.ValidationError('This time slot is already booked. Please choose another time.')
        
        return cleaned_data