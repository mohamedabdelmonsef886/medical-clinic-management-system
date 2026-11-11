from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from appointments.models import ClinicAvailability
from appointments.models import Appointment

class Command(BaseCommand):
    help = 'Generate time slots for all availability records'

    def handle(self, *args, **options):
        # Get all future availability
        availabilities = ClinicAvailability.objects.filter(
            is_available=True,
            date__gte=timezone.now().date()
        ).order_by('date')
        
        if not availabilities.exists():
            self.stdout.write(self.style.WARNING('No availability records found.'))
            self.stdout.write('Please add availability first using the dashboard.')
            return
        
        total_slots = 0
        for availability in availabilities:
            # Generate time slots
            current = datetime.combine(availability.date, availability.start_time)
            end = datetime.combine(availability.date, availability.end_time)
            
            slots_for_this_day = 0
            while current < end:
                slot_end = current + timedelta(minutes=availability.slot_duration)
                
                # Check if this slot is already booked
                is_booked = Appointment.objects.filter(
                    availability=availability,
                    appointment_time=current.time(),
                    status__in=['approved', 'confirmed', 'pending']
                ).exists()
                
                if not is_booked:
                    slots_for_this_day += 1
                
                current = slot_end
            
            total_slots += slots_for_this_day
            self.stdout.write(f"✅ {availability.location.name} - {availability.date}: {slots_for_this_day} slots available")
        
        self.stdout.write(self.style.SUCCESS(f'✅ Total {total_slots} slots available for booking!'))