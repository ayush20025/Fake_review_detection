// Main JavaScript for Fake Review Detector

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize smooth scrolling
    initSmoothScrolling();

    // Initialize form validation
    initFormValidation();

    // Initialize loading states
    initLoadingStates();

    // Initialize analytics
    initAnalytics();
});

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Loading states for buttons
function initLoadingStates() {
    const buttons = document.querySelectorAll('[data-loading-text]');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                showButtonLoading(this);
            }
        });
    });
}

function showButtonLoading(button) {
    const originalText = button.innerHTML;
    const loadingText = button.getAttribute('data-loading-text') || 'Loading...';

    button.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>${loadingText}`;
    button.disabled = true;

    // Store original text to restore later if needed
    button.setAttribute('data-original-text', originalText);
}

function hideButtonLoading(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
        button.removeAttribute('data-original-text');
    }
}

// Analytics functions
function initAnalytics() {
    // Track page views
    trackPageView();

    // Track button clicks
    trackButtonClicks();

    // Track form submissions
    trackFormSubmissions();
}

function trackPageView() {
    const page = window.location.pathname;
    console.log(`Page view: ${page}`);

    // Add your analytics code here
    // Example: gtag('config', 'GA_MEASUREMENT_ID', { page_path: page });
}

function trackButtonClicks() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            console.log(`Button clicked: ${buttonText}`);

            // Add your analytics code here
            // Example: gtag('event', 'click', { event_category: 'Button', event_label: buttonText });
        });
    });
}

function trackFormSubmissions() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const formId = this.id || 'unknown-form';
            console.log(`Form submitted: ${formId}`);

            // Add your analytics code here
            // Example: gtag('event', 'submit', { event_category: 'Form', event_label: formId });
        });
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.alert-container') || document.body;

    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    alertContainer.appendChild(alertElement);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatPercentage(num, decimals = 1) {
    return (num * 100).toFixed(decimals) + '%';
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        }).catch(() => {
            showAlert('Failed to copy to clipboard', 'danger');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Copied to clipboard!', 'success');
    }
}

// API helper functions
async function makeAPICall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Review analysis functions
function validateReviewText(text) {
    if (!text || text.trim().length === 0) {
        return { valid: false, message: 'Please enter a review to analyze' };
    }

    if (text.trim().length < 10) {
        return { valid: false, message: 'Review text should be at least 10 characters long' };
    }

    if (text.trim().length > 5000) {
        return { valid: false, message: 'Review text should be less than 5000 characters' };
    }

    return { valid: true };
}

function highlightText(text, className = 'highlight') {
    const span = document.createElement('span');
    span.className = className;
    span.textContent = text;
    return span.outerHTML;
}

// File upload functions
function validateCSVFile(file) {
    if (!file) {
        return { valid: false, message: 'No file selected' };
    }

    if (!file.name.endsWith('.csv')) {
        return { valid: false, message: 'Please select a CSV file' };
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        return { valid: false, message: 'File size should be less than 5MB' };
    }

    return { valid: true };
}

// Export functions
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = Array.from(table.querySelectorAll('tr'));
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('td, th'));
        return cells.map(cell => {
            const text = cell.textContent.trim();
            return `"${text.replace(/"/g, '""')}"`;
        }).join(',');
    }).join('\n');

    downloadCSV(csvContent, filename);
}

function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');

    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Theme functions
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit main form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const mainForm = document.querySelector('#reviewForm');
        if (mainForm) {
            mainForm.dispatchEvent(new Event('submit'));
        }
    }

    // ESC to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Performance monitoring
function measurePerformance(label, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${label} took ${end - start} milliseconds`);
    return result;
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // You can send this to your error tracking service
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You can send this to your error tracking service
});

// Initialize theme on load
initTheme();