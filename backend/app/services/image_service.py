from io import BytesIO
import warnings
from fastapi import HTTPException, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError
from app.core.config import get_settings

ACCEPTED_TYPES = {"image/jpeg", "image/png", "image/webp"}

async def read_verified_image(file: UploadFile) -> Image.Image:
    settings = get_settings()
    if file.content_type not in ACCEPTED_TYPES:
        raise HTTPException(415,"Only JPEG, PNG or WebP images are accepted")
    max_bytes = settings.max_upload_mb * 1024 * 1024
    payload = await file.read(max_bytes + 1)
    if not payload:
        raise HTTPException(400,"Empty image upload")
    if len(payload) > max_bytes:
        raise HTTPException(413,f"Maximum image upload is {settings.max_upload_mb} MB")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error",Image.DecompressionBombWarning)
            with Image.open(BytesIO(payload)) as im:
                if im.format not in ("JPEG","PNG","WEBP"):
                    raise HTTPException(415,"Decoded image format is unsupported")
                if im.width * im.height > settings.max_image_pixels:
                    raise HTTPException(413,"Image dimensions exceed pixel limit")
                im.load()
                return ImageOps.exif_transpose(im).convert("RGB")
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise HTTPException(422,"Invalid or unreadable image") from exc
