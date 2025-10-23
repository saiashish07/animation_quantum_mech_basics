// Scroll to section smoothly
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Mobile menu toggle (if needed in future)
document.addEventListener('DOMContentLoaded', function() {
    console.log('✓ Website loaded successfully');
});
