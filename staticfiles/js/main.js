/**
 * Glaucoma Detection System - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });

    // Image upload preview functionality
    initializeImageUpload();
    
    // Form validation
    initializeFormValidation();
});

/**
 * Initialize image upload preview functionality
 */
function initializeImageUpload() {
    const uploadArea = document.getElementById('uploadArea');
    
    // If upload area exists on page
    if (uploadArea) {
        const fileInput = document.querySelector('input[type="file"]');
        const imagePreview = document.getElementById('imagePreview');
        const previewImg = imagePreview?.querySelector('img');
        const removeButton = document.getElementById('removeImage');
        const analyzeBtn = document.getElementById('analyzeBtn');
        
        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadArea.classList.add('highlight');
        }
        
        function unhighlight() {
            uploadArea.classList.remove('highlight');
        }
        
        // Handle file drop
        uploadArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length) {
                fileInput.files = files;
                displayPreview(files[0]);
            }
        }
        
        // Handle file selection through input
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                if (this.files.length) {
                    displayPreview(this.files[0]);
                }
            });
        }
        
        // Display image preview
        function displayPreview(file) {
            if (!file.type.match('image.*')) {
                showAlert('Please select an image file.', 'danger');
                return;
            }
            
            const reader = new FileReader();
            
            reader.onload = function(e) {
                if (previewImg) {
                    previewImg.src = e.target.result;
                    imagePreview.classList.remove('d-none');
                    
                    // Enable analyze button
                    if (analyzeBtn) {
                        analyzeBtn.disabled = false;
                    }
                }
            }
            
            reader.readAsDataURL(file);
        }
        
        // Remove image preview
        if (removeButton) {
            removeButton.addEventListener('click', function() {
                if (fileInput) fileInput.value = '';
                if (imagePreview) imagePreview.classList.add('d-none');
                if (previewImg) previewImg.src = '';
                
                // Disable analyze button
                if (analyzeBtn) {
                    analyzeBtn.disabled = true;
                }
            });
        }
    }
}

/**
 * Show an alert message
 */
function showAlert(message, type = 'info') {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type} alert-dismissible fade show`;
    alertBox.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to the messages container or create one
    let messagesContainer = document.querySelector('.messages');
    if (!messagesContainer) {
        messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages';
        document.querySelector('main').prepend(messagesContainer);
    }
    
    messagesContainer.appendChild(alertBox);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertBox.classList.remove('show');
        setTimeout(() => alertBox.remove(), 150);
    }, 5000);
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
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
}