// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const submitBtn = document.getElementById('submit-btn');
    const resultsSection = document.getElementById('results-section');
    const originalImage = document.getElementById('original-image');
    const maskImage = document.getElementById('mask-image');
    const overlayImage = document.getElementById('overlay-image');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    
    // Prevent default drag behaviors
    // Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

// Handle selected files
fileInput.addEventListener('change', handleFiles);

// Handle form submission
submitBtn.addEventListener('click', uploadFile);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    dropArea.classList.add('highlight');
}

function unhighlight() {
    dropArea.classList.remove('highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(e) {
    let files;
    if (e.dataTransfer) {
        files = e.dataTransfer.files;
    } else if (e.target.files) {
        files = e.target.files;
    }
    
    if (files && files.length > 0) {
        const file = files;
        
        // Check if file type is allowed
        const fileType = file.name.split('.').pop().toLowerCase();
        const allowedTypes = ['nii', 'gz', 'png', 'jpg', 'jpeg'];
        
        if (!allowedTypes.includes(fileType) && !(fileType === 'gz' && file.name.includes('.nii.gz'))) {
            showError('Invalid file type. Please upload a NIfTI (.nii, .nii.gz) or image file (.png, .jpg, .jpeg).');
            return;
        }
        
        fileName.textContent = file.name;
        submitBtn.disabled = false;
        hideError();
    }
}

function uploadFile() {
    if (fileInput.files.length === 0) {
        showError('Please select a file first.');
        return;
    }
    
    const file = fileInput.files;
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        hideLoading();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Display results
        originalImage.src = data.original;
        maskImage.src = data.mask;
        overlayImage.src = data.overlay;
        
        // Show results section
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        hideLoading();
        showError('Error processing the image: ' + error.message);
        console.error('Error:', error);
    });
}

function showLoading() {
    loading.style.display = 'flex';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.textContent = '';
    errorMessage.style.display = 'none';
}
});