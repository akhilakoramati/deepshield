import uuid
import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from ..core.config import MAX_FILE_SIZE, UPLOAD_DIR
from ..models.media_file import UploadedFile

ALLOWED_TYPES = {"image", "audio", "video"}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".mp4", ".mov", ".webm"}


def _has_valid_image_signature(content: bytes, suffix: str) -> bool:
    expected = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}.get(suffix)
    if expected is None:
        return False
    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()
            return image.format == expected
    except (UnidentifiedImageError, OSError):
        return False


def _has_media_signature(content: bytes, suffix: str, media_type: str) -> bool:
    signatures = {
        ".wav": content.startswith(b"RIFF") and content[8:12] == b"WAVE",
        ".flac": content.startswith(b"fLaC"),
        ".ogg": content.startswith(b"OggS"),
        ".mp3": content.startswith(b"ID3") or (len(content) > 1 and content[0] == 0xFF and content[1] & 0xE0 == 0xE0),
        ".m4a": len(content) >= 12 and content[4:8] == b"ftyp" and b"M4A" in content[8:32],
        ".mp4": len(content) >= 12 and content[4:8] == b"ftyp",
        ".mov": len(content) >= 12 and content[4:8] == b"ftyp",
        ".webm": content.startswith(b"\x1a\x45\xdf\xa3"),
    }
    if not signatures.get(suffix, False):
        return False
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        return True
    with tempfile.NamedTemporaryFile(suffix=suffix) as temporary:
        temporary.write(content)
        temporary.flush()
        stream = "a:0" if media_type == "audio" else "v:0"
        result = subprocess.run([ffprobe, "-v", "error", "-select_streams", stream, "-show_entries", "stream=codec_type", "-of", "csv=p=0", temporary.name], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == media_type


async def store_upload(file: UploadFile, user_id: int, database: Session) -> UploadedFile:
    suffix = Path(file.filename or "").suffix.lower()
    media_type = (file.content_type or "").split("/")[0]
    if suffix not in ALLOWED_EXTENSIONS or media_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image, audio, or video file type")
    content = await file.read(MAX_FILE_SIZE + 1)
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Files must be 50 MB or smaller")
    if media_type == "image" and not _has_valid_image_signature(content, suffix):
        raise HTTPException(status_code=415, detail="File contents do not match the declared image format")
    if media_type in {"audio", "video"} and not _has_media_signature(content, suffix, media_type):
        raise HTTPException(status_code=415, detail="File contents do not match the declared media format")
    stored_name = f"{uuid.uuid4().hex}{suffix}"
    (UPLOAD_DIR / stored_name).write_bytes(content)
    record = UploadedFile(user_id=user_id, original_name=file.filename or "unnamed file", stored_name=stored_name, media_type=media_type, size_bytes=len(content))
    database.add(record)
    database.commit()
    database.refresh(record)
    return record
