document.addEventListener('DOMContentLoaded', function() {
    // Tooltip initialization
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            this.setAttribute('data-tooltip-active', 'true');
        });
        tooltip.addEventListener('mouseleave', function() {
            this.removeAttribute('data-tooltip-active');
        });
    });

    // Form submission animation
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
            }
        });
    }

    // Animate probability meter
    const meterFill = document.querySelector('.meter-fill');
    if (meterFill) {
        // The width is already set inline from the template
        // Add animation class
        meterFill.classList.add('animate-meter');
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});