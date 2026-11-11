// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add any custom JavaScript here
    console.log('Medical Clinic Website loaded successfully');
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});