import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Create placeholder images for the website'

    def handle(self, *args, **options):
        # Create images directory
        images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        self.stdout.write(self.style.SUCCESS('Created images directory'))
        
        # Create default avatar SVG
        avatar_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <circle cx="30" cy="30" r="30" fill="#e0edff"/>
  <circle cx="30" cy="22" r="12" fill="#0056b3"/>
  <ellipse cx="30" cy="42" rx="16" ry="12" fill="#0056b3"/>
  <circle cx="25" cy="20" r="2.5" fill="white"/>
  <circle cx="35" cy="20" r="2.5" fill="white"/>
  <path d="M26 26 Q30 28 34 26" stroke="white" stroke-width="2" fill="none"/>
</svg>'''
        
        with open(os.path.join(images_dir, 'default-avatar.png'), 'w') as f:
            f.write(avatar_svg)
        
        self.stdout.write(self.style.SUCCESS('Created default avatar'))
        
        # Create doctor about placeholder
        doctor_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
  <rect width="500" height="500" fill="#f0f7ff" rx="20"/>
  <circle cx="250" cy="180" r="100" fill="#0056b3" opacity="0.1"/>
  <circle cx="250" cy="180" r="70" fill="#0056b3" opacity="0.2"/>
  <circle cx="250" cy="155" r="35" fill="#0056b3"/>
  <path d="M200 240 Q250 340 300 240" stroke="#0056b3" stroke-width="25" fill="none" opacity="0.3"/>
  <path d="M210 250 Q250 360 290 250" stroke="#0056b3" stroke-width="18" fill="none" opacity="0.2"/>
  <text x="250" y="420" font-family="Arial" font-size="28" fill="#0056b3" text-anchor="middle" font-weight="bold">Dr. Sarah Johnson</text>
  <text x="250" y="460" font-family="Arial" font-size="18" fill="#6c757d" text-anchor="middle">Board Certified Internal Medicine Specialist</text>
</svg>'''
        
        with open(os.path.join(images_dir, 'doctor-about.png'), 'w') as f:
            f.write(doctor_svg)
        
        self.stdout.write(self.style.SUCCESS('Created doctor about placeholder'))
        
        # Create favicon.ico (simple approach - use a small PNG)
        favicon_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="16" fill="#0056b3"/>
  <circle cx="16" cy="12" r="6" fill="white"/>
  <path d="M10 22 Q16 26 22 22" stroke="white" stroke-width="3" fill="none"/>
  <circle cx="14" cy="11" r="1.5" fill="#0056b3"/>
  <circle cx="18" cy="11" r="1.5" fill="#0056b3"/>
</svg>'''
        
        with open(os.path.join(images_dir, 'favicon.ico'), 'w') as f:
            f.write(favicon_svg)
        
        self.stdout.write(self.style.SUCCESS('Created favicon'))
        
        self.stdout.write(self.style.SUCCESS('All placeholder images created successfully!'))