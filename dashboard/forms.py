from django import forms
from services.models import Service
from testimonials.models import Testimonial
from blog.models import BlogPost
from core.models import SiteSettings
from appointments.models import ClinicAvailability

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'short_description', 'icon', 'image', 'price', 'duration', 'is_featured', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description of the service'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description (max 300 chars)'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Font Awesome icon class (e.g., fa-heartbeat)'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30 minutes'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Service Title',
            'description': 'Description',
            'short_description': 'Short Description',
            'icon': 'Icon Class',
            'image': 'Service Image',
            'price': 'Price (Optional)',
            'duration': 'Duration (Optional)',
            'is_featured': 'Featured Service',
            'is_active': 'Active',
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['patient_name', 'patient_image', 'patient_condition', 'review', 'rating', 'is_featured', 'is_approved']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient full name'}),
            'patient_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'patient_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Dental Patient, Orthopedic Patient'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Patient review/testimonial'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': '1-5'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'patient_name': 'Patient Name',
            'patient_image': 'Patient Photo',
            'patient_condition': 'Patient Condition',
            'review': 'Review',
            'rating': 'Rating (1-5)',
            'is_featured': 'Featured Testimonial',
            'is_approved': 'Approved',
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'featured_image', 'excerpt', 'content', 'author', 'is_published', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog post title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'excerpt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief excerpt (max 300 chars)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Full blog post content'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author name'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Post Title',
            'category': 'Category',
            'featured_image': 'Featured Image',
            'excerpt': 'Excerpt',
            'content': 'Content',
            'author': 'Author',
            'is_published': 'Published',
            'published_date': 'Publish Date',
        }



class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical Clinic'}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical Clinic'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. John Doe'}),
            'doctor_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical Specialist'}),
            'doctor_biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write a comprehensive biography...'}),
            'doctor_qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'MD, FACP, Board Certified...'}),
            'doctor_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '15+ years of clinical experience'}),
            'doctor_certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Board Certified, ACLS Certified...'}),
            'doctor_achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Published research, awards...'}),
            'doctor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'doctor@clinic.com'}),
            'doctor_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'clinic_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '123 Medical Drive, Suite 200, Health City'}),
            'clinic_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'clinic_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'info@clinic.com'}),
            'working_hours': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Monday - Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 2:00 PM\nSunday: Closed'}),
            'google_maps_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '<iframe src="https://www.google.com/maps/embed?..."></iframe>'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/yourpage'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourprofile'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourprofile'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/company/yourpage'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/yourchannel'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15'}),
            'happy_patients': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5000'}),
            'operations_completed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2000'}),
            'awards_won': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all file/image fields NOT required
        self.fields['site_logo'].required = False
        self.fields['site_favicon'].required = False
        self.fields['doctor_image'].required = False


class ClinicAvailabilityForm(forms.ModelForm):
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

# class SiteSettingsForm(forms.ModelForm):
#     class Meta:
#         model = SiteSettings
#         fields = '__all__'
#         widgets = {
#             # Site Information
#             'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical Clinic'}),
#             'site_logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
#             'site_favicon': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            
#             # Doctor Information
#             'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. John Doe'}),
#             'doctor_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical Specialist'}),
#             'doctor_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
#             'doctor_biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Write a comprehensive biography...'}),
#             'doctor_qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'MD, FACP, Board Certified...'}),
#             'doctor_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '15+ years of clinical experience'}),
#             'doctor_certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Board Certified, ACLS Certified...'}),
#             'doctor_achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Published research, awards...'}),
#             'doctor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'doctor@clinic.com'}),
#             'doctor_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            
#             # Clinic Information
#             'clinic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Advanced Medical Clinic'}),
#             'clinic_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '123 Medical Drive, Suite 200, Health City'}),
#             'clinic_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
#             'clinic_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'info@clinic.com'}),
#             'working_hours': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Monday - Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 2:00 PM\nSunday: Closed'}),
#             'google_maps_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '<iframe src="https://www.google.com/maps/embed?..."></iframe>'}),
            
#             # Social Media
#             'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/yourpage'}),
#             'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourprofile'}),
#             'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourprofile'}),
#             'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/company/yourpage'}),
#             'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/yourchannel'}),
            
#             # Statistics
#             'years_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15'}),
#             'happy_patients': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5000'}),
#             'operations_completed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2000'}),
#             'awards_won': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}),
#         }
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             # Make all file fields not required
#             for field_name in ['site_logo', 'site_favicon', 'doctor_image']:
#                 if field_name in self.fields:
#                     self.fields[field_name].required = False
#         labels = {
#             'site_name': 'Site Name',
#             'site_logo': 'Site Logo',
#             'site_favicon': 'Favicon',
#             'doctor_name': 'Doctor Full Name',
#             'doctor_title': 'Doctor Title',
#             'doctor_image': 'Doctor Profile Image',
#             'doctor_biography': 'Biography',
#             'doctor_qualifications': 'Qualifications',
#             'doctor_experience': 'Experience',
#             'doctor_certifications': 'Certifications',
#             'doctor_achievements': 'Achievements',
#             'doctor_email': 'Doctor Email',
#             'doctor_phone': 'Doctor Phone',
#             'clinic_name': 'Clinic Name',
#             'clinic_address': 'Clinic Address',
#             'clinic_phone': 'Clinic Phone',
#             'clinic_email': 'Clinic Email',
#             'working_hours': 'Working Hours',
#             'google_maps_embed': 'Google Maps Embed Code',
#             'facebook_url': 'Facebook URL',
#             'twitter_url': 'Twitter URL',
#             'instagram_url': 'Instagram URL',
#             'linkedin_url': 'LinkedIn URL',
#             'youtube_url': 'YouTube URL',
#             'years_experience': 'Years of Experience',
#             'happy_patients': 'Number of Happy Patients',
#             'operations_completed': 'Operations/Procedures Completed',
#             'awards_won': 'Awards Won',
#         }