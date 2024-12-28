# Django Media Manager

A Django-based web application for managing media files with a modern, user-friendly interface. This application allows users to upload, view, download, and delete various types of media files (images, audio, and video) with real-time feedback and interactive features.

## Features

- Upload multiple files simultaneously (up to 10 files)
- Support for various file types:
  - Images (jpeg, png, gif)
  - Audio (mp3)
  - Video (mp4)
- File size restrictions:
  - Minimum: 100KB
  - Maximum: 10MB
- Real-time file management:
  - View files in modal windows
  - Download files
  - Delete files with confirmation
- Modern UI with responsive design
- Toast notifications for user feedback
- No page reloads required (AJAX-based operations)

## Technologies Used

### Backend
- Django 5.1.4
- Python 3.x
- SQLite database

### Frontend
- Bootstrap 5.1.3 - CSS framework for responsive design
- SweetAlert2 - Beautiful, responsive, customizable alert dialogs
- JavaScript (ES6+) - For dynamic interactions

### JavaScript Libraries
1. **Bootstrap 5.1.3**
   - Purpose: Frontend framework for responsive design
   - CDN: `https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css`
   - JS Bundle: `https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js`
   - Features used:
     - Modal dialogs
     - Responsive tables
     - Buttons and alerts
     - Grid system

2. **SweetAlert2**
   - Purpose: Enhanced alerts and confirmations
   - CDN: `https://cdn.jsdelivr.net/npm/sweetalert2@11`
   - Features used:
     - Delete confirmations
     - Toast notifications
     - Success/Error messages
     - Custom styled dialogs