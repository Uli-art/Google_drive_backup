
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
root_folder = "GoogleWorkspace/GoogleDrive/"

MIME_TYPES = {
    'application/vnd.google-apps.document':
        ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
    'application/vnd.google-apps.spreadsheet':
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
    'application/vnd.google-apps.presentation':
        ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx')
}
