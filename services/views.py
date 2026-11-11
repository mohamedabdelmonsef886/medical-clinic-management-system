from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Service

def service_list(request):
    """Display all services with pagination"""
    # Get all active services
    all_services = Service.objects.filter(is_active=True)
    
    # Get featured services (from all services, not paginated)
    featured_services = all_services.filter(is_featured=True)[:3]
    
    # Pagination - use the filtered queryset
    paginator = Paginator(all_services, 9)  # 9 services per page
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    # Get categories from all services (not paginated)
    categories = []
    if hasattr(Service, 'category'):
        categories = all_services.values_list('category', flat=True).distinct()
    
    context = {
        'services': services,
        'featured_services': featured_services,
        'categories': categories,
        'total_services': all_services.count(),
    }
    return render(request, 'services/services.html', context)

def service_detail(request, slug):
    """Display service detail"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Get related services (same category if available)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/service_detail.html', context)