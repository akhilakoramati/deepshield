from .base import DetectorResult


def detect_video(file_path: str) -> DetectorResult:
    """Model seam for the future XceptionNet + LSTM video detector."""
    return DetectorResult("FAKE", 88.4, "completed", "Mock video detection completed; model integration is pending.")
