from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class ClinicLocation(models.Model):
    """Model for clinic locations"""
    name = models.CharField(max_length=200, help_text="e.g., Main Branch, Downtown Clinic")
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        ordering = ['city', 'name']

class ClinicAvailability(models.Model):
    """Model for clinic availability - specific dates and locations"""
    location = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes per slot")
    max_patients = models.IntegerField(default=10, help_text="Maximum number of patients per day")
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Special notes for this date (e.g., 'Special clinic', 'Holiday hours')")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.location.name} - {self.date} ({self.start_time} - {self.end_time})"

def get_available_slots(self):
        """Get all available time slots for this availability"""
        from datetime import datetime, timedelta
        slots = []
        current = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        
        while current < end:
            slot_end = current + timedelta(minutes=self.slot_duration)
            # Check if this slot is already booked
            is_booked = Appointment.objects.filter(
                availability=self,
                appointment_time=current.time(),
                status__in=['approved', 'confirmed', 'pending']
            ).exists()
            
            slots.append({
                'start': current.time(),
                'end': slot_end.time(),
                'is_booked': is_booked,
                'formatted': f"{current.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}"
            })
            current = slot_end
        
        return slots
    
def get_available_slots_count(self):
        """Get count of available slots"""
        return len([slot for slot in self.get_available_slots() if not slot['is_booked']])
    
class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['location', 'date']

class ClinicSchedule(models.Model):
    """Model for clinic availability schedule"""
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    location = models.ForeignKey(ClinicLocation, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.IntegerField(default=30, help_text="Duration in minutes per slot")
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.location.name} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"
    
    class Meta:
        ordering = ['location', 'day_of_week', 'start_time']
        unique_together = ['location', 'day_of_week']

class TimeSlot(models.Model):
    """Model for individual time slots"""
    schedule = models.ForeignKey(ClinicSchedule, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.schedule.location.name} - {self.date} ({self.start_time} - {self.end_time})"
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['schedule', 'date', 'start_time']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Patient Information
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=20)
    patient_email = models.EmailField()
    patient_age = models.IntegerField(blank=True, null=True)
    
    # Appointment Details
    location = models.ForeignKey(ClinicLocation, on_delete=models.SET_NULL, null=True, blank=True)
    availability = models.ForeignKey(ClinicAvailability, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)  # Will be set by admin
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_appointment_details(self):
        """Get formatted appointment details for SMS"""
        location_name = self.location.name if self.location else "Not assigned"
        date_str = self.appointment_date.strftime("%A, %B %d, %Y")
        time_str = self.appointment_time.strftime("%I:%M %p") if self.appointment_time else "To be confirmed"
        
        return {
            'patient': self.patient_name,
            'location': location_name,
            'date': date_str,
            'time': time_str,
            'address': self.location.address if self.location else "Not assigned",
            'status': self.get_status_display()
        }
    # class Meta:
    #     ordering = ['-appointment_date', 'appointment_time']