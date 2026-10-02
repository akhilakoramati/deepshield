from .base import DetectorResult


def detect_image(file_path: str) -> DetectorResult:
    """Model seam for the future EfficientNet image detector."""
    return DetectorResult("FAKE", 94.6, "completed", "Mock image detection completed; model integration is pending.")
