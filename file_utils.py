"""
File Upload and Management Utilities for EcoFreonTrack
Handles secure file uploads, storage, and retrieval for documentation
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from models import db, Document

# Allowed file extensions for different document types
ALLOWED_EXTENSIONS = {
    'Certification': {'pdf', 'jpg', 'jpeg', 'png'},
    'Invoice': {'pdf', 'jpg', 'jpeg', 'png'},
    'Photo': {'jpg', 'jpeg', 'png', 'gif', 'bmp'},
    'Report': {'pdf', 'doc', 'docx', 'txt'},
    'Manual': {'pdf', 'doc', 'docx'},
    'Warranty': {'pdf', 'jpg', 'jpeg', 'png'},
    'Inspection': {'pdf', 'jpg', 'jpeg', 'png'},
    'Other': {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'txt', 'xls', 'xlsx'}
}

# MIME type mapping
MIME_TYPES = {
    'pdf': 'application/pdf',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'txt': 'text/plain'
}

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # bytes


def get_upload_folder(base_folder='uploads'):
    """Get or create the uploads folder"""
    upload_path = os.path.join(os.getcwd(), base_folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    return upload_path


def allowed_file(filename, document_type='Other'):
    """Check if file extension is allowed for the document type"""
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    allowed = ALLOWED_EXTENSIONS.get(document_type, ALLOWED_EXTENSIONS['Other'])
    return ext in allowed


def get_mime_type(filename):
    """Get MIME type from filename extension"""
    if '.' not in filename:
        return 'application/octet-stream'

    ext = filename.rsplit('.', 1)[1].lower()
    return MIME_TYPES.get(ext, 'application/octet-stream')


def generate_unique_filename(original_filename):
    """Generate a unique filename using UUID to prevent collisions"""
    # Get file extension
    ext = ''
    if '.' in original_filename:
        ext = '.' + original_filename.rsplit('.', 1)[1].lower()

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"


def save_uploaded_file(file, document_type='Other', subfolder=None):
    """
    Save an uploaded file to the uploads directory

    Args:
        file: FileStorage object from request.files
        document_type: Type of document (used for validation)
        subfolder: Optional subfolder within uploads (e.g., 'technicians', 'equipment')

    Returns:
        tuple: (success: bool, filepath: str or error_message: str, filesize: int)
    """
    if not file or file.filename == '':
        return False, 'No file provided', 0

    # Check file extension
    if not allowed_file(file.filename, document_type):
        allowed = ALLOWED_EXTENSIONS.get(document_type, ALLOWED_EXTENSIONS['Other'])
        return False, f'File type not allowed. Allowed: {", ".join(allowed)}', 0

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, f'File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.1f} MB', 0

    # Generate unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)

    # Determine upload path
    upload_folder = get_upload_folder()
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, unique_filename)

    # Save file
    try:
        file.save(file_path)

        # Return relative path for database storage
        relative_path = os.path.relpath(file_path, get_upload_folder())
        return True, relative_path, file_size

    except Exception as e:
        return False, f'Error saving file: {str(e)}', 0


def create_document_record(file, document_type, description='',
                           equipment_id=None, technician_id=None,
                           service_log_id=None, leak_inspection_id=None,
                           refrigerant_transaction_id=None,
                           document_date=None, expiration_date=None,
                           uploaded_by=None, subfolder=None):
    """
    Save a file and create a database record

    Args:
        file: FileStorage object from request.files
        document_type: Type of document (Certification, Invoice, Photo, etc.)
        description: Optional description
        equipment_id: Optional link to equipment
        technician_id: Optional link to technician
        service_log_id: Optional link to service log
        leak_inspection_id: Optional link to leak inspection
        refrigerant_transaction_id: Optional link to refrigerant transaction
        document_date: Date on the document
        expiration_date: Expiration date (for certifications, etc.)
        uploaded_by: Name of person uploading
        subfolder: Subfolder in uploads directory

    Returns:
        tuple: (success: bool, document_id: int or error_message: str)
    """
    # Save file
    success, result, file_size = save_uploaded_file(file, document_type, subfolder)

    if not success:
        return False, result

    file_path = result
    original_filename = secure_filename(file.filename)
    mime_type = get_mime_type(original_filename)

    # Create database record
    try:
        document = Document(
            filename=os.path.basename(file_path),
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            document_type=document_type,
            description=description,
            equipment_id=equipment_id,
            technician_id=technician_id,
            service_log_id=service_log_id,
            leak_inspection_id=leak_inspection_id,
            refrigerant_transaction_id=refrigerant_transaction_id,
            document_date=document_date,
            expiration_date=expiration_date,
            uploaded_by=uploaded_by,
            status='Active'
        )

        db.session.add(document)
        db.session.commit()

        return True, document.id

    except Exception as e:
        db.session.rollback()
        # Try to delete the uploaded file if database insert fails
        try:
            full_path = os.path.join(get_upload_folder(), file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except:
            pass

        return False, f'Error creating document record: {str(e)}'


def get_document_path(document_id):
    """Get the full filesystem path for a document"""
    document = Document.query.get(document_id)
    if not document:
        return None

    return os.path.join(get_upload_folder(), document.file_path)


def delete_document(document_id):
    """
    Delete a document file and database record

    Args:
        document_id: ID of document to delete

    Returns:
        tuple: (success: bool, message: str)
    """
    document = Document.query.get(document_id)
    if not document:
        return False, 'Document not found'

    # Delete file from filesystem
    file_path = get_document_path(document_id)
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return False, f'Error deleting file: {str(e)}'

    # Delete database record
    try:
        db.session.delete(document)
        db.session.commit()
        return True, 'Document deleted successfully'
    except Exception as e:
        db.session.rollback()
        return False, f'Error deleting document record: {str(e)}'


def get_documents_by_entity(equipment_id=None, technician_id=None,
                            service_log_id=None, leak_inspection_id=None,
                            refrigerant_transaction_id=None, document_type=None):
    """
    Get all documents associated with an entity

    Args:
        equipment_id: Filter by equipment
        technician_id: Filter by technician
        service_log_id: Filter by service log
        leak_inspection_id: Filter by leak inspection
        refrigerant_transaction_id: Filter by refrigerant transaction
        document_type: Optional filter by document type

    Returns:
        List of Document objects
    """
    query = Document.query.filter_by(status='Active')

    if equipment_id:
        query = query.filter_by(equipment_id=equipment_id)
    if technician_id:
        query = query.filter_by(technician_id=technician_id)
    if service_log_id:
        query = query.filter_by(service_log_id=service_log_id)
    if leak_inspection_id:
        query = query.filter_by(leak_inspection_id=leak_inspection_id)
    if refrigerant_transaction_id:
        query = query.filter_by(refrigerant_transaction_id=refrigerant_transaction_id)
    if document_type:
        query = query.filter_by(document_type=document_type)

    return query.order_by(Document.uploaded_at.desc()).all()


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_document_icon(mime_type):
    """Get an icon class/emoji for document type"""
    icons = {
        'application/pdf': '📄',
        'image/jpeg': '🖼️',
        'image/png': '🖼️',
        'image/gif': '🖼️',
        'application/msword': '📝',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '📝',
        'text/plain': '📃',
        'application/vnd.ms-excel': '📊',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '📊'
    }
    return icons.get(mime_type, '📎')
