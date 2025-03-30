import os
import uuid

from fastapi import APIRouter, status, UploadFile, File, HTTPException, BackgroundTasks

from app.api.schemas.content import ContentResponseSchema
from app.api.constants.content.docs import DOCS
from app.api.constants.content.validations import validations
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

router = APIRouter(
    prefix="/content",
    tags=["Content Management"],
    redirect_slashes=False,
)
def save_file(file_path: str, file_content: bytes):
    with open(file_path, "wb") as f:
        f.write(file_content)

@router.post(
    "/upload/image/",
    status_code=status.HTTP_201_CREATED,
    summary="Upload an image",
    description=DOCS["image"],
    response_model=ContentResponseSchema,
)
async def upload_image(image: UploadFile = File(...)) -> ContentResponseSchema:
    if image.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image filename is required",
        )
    file_extension = image.filename.split(".")[-1].lower()
    image.filename = uuid.uuid4().hex + "." + file_extension
    if file_extension not in validations["image"]["support"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    file_content = await image.read()
    if len(file_content) > validations["image"]["max_size"]:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds limit",
        )

    file_path = os.path.join(validations["image"]["path"], image.filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return ContentResponseSchema(
        upload_to=file_path, link=settings.BASE_URL+ '/' + file_path
    )


@router.post(
    "/upload/video/",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a video",
    description=DOCS["video"],
    response_model=ContentResponseSchema,
)
async def upload_video(video: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()) -> ContentResponseSchema:
    if video.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video filename is required",
        )
    file_extension = video.filename.split(".")[-1].lower()
    video.filename = uuid.uuid4().hex + "." + file_extension
    if file_extension not in validations["video"]["support"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    file_content = await video.read()
    if len(file_content) > validations["video"]["max_size"]:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds limit",
        )

    file_path = os.path.join(validations["video"]["path"], video.filename)
    background_tasks.add_task(save_file, file_path, file_content)
    return ContentResponseSchema(
        upload_to=file_path, link=settings.BASE_URL + '/' + file_path
    )

@router.post(
    "/upload/document/",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
    description=DOCS["document"],
    response_model=ContentResponseSchema,
)
async def upload_document(
        document: UploadFile = File(...),
        background_tasks: BackgroundTasks = BackgroundTasks()
) -> ContentResponseSchema:
    if document.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document filename is required",
        )
    file_extension = document.filename.split(".")[-1].lower()
    document.filename = uuid.uuid4().hex + "." + file_extension
    if file_extension not in validations["document"]["support"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    file_content = await document.read()
    if len(file_content) > validations["document"]["max_size"]:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds limit",
        )

    file_path = os.path.join(validations["document"]["path"], document.filename)
    background_tasks.add_task(save_file, file_path, file_content)
    return ContentResponseSchema(
        upload_to=file_path, link=settings.BASE_URL + '/' + file_path
    )
