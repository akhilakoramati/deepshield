from collections.abc import Callable

from .audio_detector import detect_audio
from .base import DetectorResult
from .image_detector import detect_image
from .video_detector import detect_video

Detector = Callable[[str], DetectorResult]

_DETECTORS: dict[str, Detector] = {
    "image": detect_image,
    "audio": detect_audio,
    "video": detect_video,
}


def get_detector(media_type: str) -> Detector:
    try:
        return _DETECTORS[media_type]
    except KeyError:
        raise ValueError(f"No detector is registered for media type: {media_type}") from None
