validations: dict[str, dict] = {
    "image": {
        "path": "media/uploads/images",
        "support": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
        "max_size": 20 * 1024 * 1024,  # 20MB
    },
    "video": {
        "path": "media/uploads/videos",
        "support": ["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"],
        "max_size": 1_000 * 1024 * 1024,  # 1000MB
    },
    "document": {
        "path": "media/uploads/documents",
        "support": [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "txt",
            "csv",
            "zip",
            "rar",
        ],
        "max_size": 200 * 1024 * 1024,  # 200MB
    },
}
