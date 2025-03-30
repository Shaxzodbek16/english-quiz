DOCS: dict[str, str] = {
    "image": """IMAGES_VALIDATION:
Validation rules for image uploads.
- path: Directory where images are stored ("media/uploads/images").
- support: Allowed image formats - ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"].
- max_size: Maximum file size allowed (10MB).
""",
    "video": """VIDEOS_VALIDATION:
Validation rules for video uploads.

- path: Directory where videos are stored ("media/uploads/videos").
- support: Allowed video formats - ["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"].
- max_size: Maximum file size allowed (100MB).
""",
    "document": """DOCUMENTS_VALIDATION:
Validation rules for document uploads.

- path: Directory where documents are stored ("media/uploads/documents").
- support: Allowed document formats - ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv"].
- max_size: Maximum file size allowed (50MB).
""",
}
