from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='home'),
    
    # Appointments
    path('appointments/', views.appointment_list, name='appointments'),
    path('appointments/<int:pk>/detail/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/update-status/', views.appointment_update_status, name='appointment_update_status'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    
    # Services
    path('services/', views.service_list, name='services'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Testimonials
    path('testimonials/', views.testimonial_list, name='testimonials'),
    path('testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),
    
    # Blog
    path('blog/', views.blog_list, name='blog'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    
    # Contacts
    path('contacts/', views.contact_list, name='contacts'),
    path('contacts/<int:pk>/detail/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # Settings
    path('settings/', views.settings_edit, name='settings'),
    # Locations
    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.location_add, name='location_add'),
    path('locations/<int:pk>/edit/', views.location_edit, name='location_edit'),
    path('locations/<int:pk>/delete/', views.location_delete, name='location_delete'),
    # Availability
    path('availability/', views.availability_list, name='availability_list'),
    path('availability/add/', views.availability_add, name='availability_add'),
    path('availability/<int:pk>/edit/', views.availability_edit, name='availability_edit'),
    path('availability/<int:pk>/delete/', views.availability_delete, name='availability_delete'),
]