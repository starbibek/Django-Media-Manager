// Toast function using SweetAlert2
function showToast(message, type = 'success') {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });

    Toast.fire({
        icon: type,
        title: message
    });
}

// Function to update the file list
function updateFileList(files) {
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';
    
    files.forEach(file => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${file.filename}</td>
            <td>${file.category}</td>
            <td>${formatFileSize(file.size)}</td>
            <td>${new Date(file.uploaded_at).toLocaleString()}</td>
            <td>
                <button onclick="viewFile('${file.file}', '${file.category}')" 
                        class="btn btn-sm btn-info">View</button>
                <a href="/download/${file.id}/" 
                   class="btn btn-sm btn-success">Download</a>
                <button onclick="deleteFile(${file.id})" 
                        class="btn btn-sm btn-danger">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// View file in modal
function viewFile(url, type) {
    const content = document.getElementById('viewModalContent');
    content.innerHTML = '';

    if (type === 'IMAGE') {
        content.innerHTML = `<img src="${url}" class="modal-image">`;
    } else if (type === 'VIDEO') {
        content.innerHTML = `
            <video controls class="w-100">
                <source src="${url}" type="video/mp4">
            </video>`;
    } else if (type === 'AUDIO') {
        content.innerHTML = `
            <audio controls class="w-100">
                <source src="${url}" type="audio/mpeg">
            </audio>`;
    }

    new bootstrap.Modal(document.getElementById('viewModal')).show();
}

// Delete file function
async function deleteFile(pk) {
    const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel'
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`/delete/${pk}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                showToast("Your file has been deleted.", 'success');
                updateFileList(data.files);
            } else {
                showToast("Failed to delete the file.", 'danger');
            }
        } catch (error) {
            showToast("An error occurred while deleting the file.", 'danger');
        }
    }
}

// Initialize form submission handler
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                showToast(result.message);
                updateFileList(result.files);
                bootstrap.Modal.getInstance(document.getElementById('uploadModal')).hide();
                e.target.reset();
            } else {
                showToast(result.message, 'danger');
            }
        } catch (error) {
            showToast('An error occurred while uploading', 'danger');
        }
    });
}); 