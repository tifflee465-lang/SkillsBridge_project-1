// Main JavaScript for SkillBridge

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Skill tag input functionality
    const skillInputs = document.querySelectorAll('.skill-input');
    skillInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const skill = this.value.trim();
                if (skill) {
                    addSkillTag(skill, this);
                    this.value = '';
                }
            }
        });
    });

    // Location autocomplete (simplified)
    const locationInput = document.querySelector('input[name="location"]');
    if (locationInput) {
        locationInput.addEventListener('input', debounce(function() {
            // In a real app, you would fetch location suggestions here
            console.log('Fetching location suggestions for:', this.value);
        }, 300));
    }
});

// Utility function to add skill tags
function addSkillTag(skill, inputElement) {
    const container = inputElement.closest('.skill-input-container');
    const tagsContainer = container.querySelector('.skill-tags');
    
    if (!tagsContainer) return;
    
    const tag = document.createElement('span');
    tag.className = 'badge bg-primary me-2 mb-2';
    tag.innerHTML = `${skill} <button type="button" class="btn-close btn-close-white ms-1" style="font-size: 0.5rem;" onclick="this.parentElement.remove()"></button>`;
    
    tagsContainer.appendChild(tag);
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Match percentage calculation (simplified)
function calculateMatch(userSkills, otherSkills) {
    const userSkillsSet = new Set(userSkills);
    const otherSkillsSet = new Set(otherSkills);
    
    const intersection = [...userSkillsSet].filter(x => otherSkillsSet.has(x));
    const union = new Set([...userSkillsSet, ...otherSkillsSet]);
    
    return union.size > 0 ? Math.round((intersection.length / union.size) * 100) : 0;
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Image preview for profile picture upload
function previewProfilePicture(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.getElementById('profile-picture-preview');
        
        reader.onload = function(e) {
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}