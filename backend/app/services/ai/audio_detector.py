from .base import DetectorResult


def detect_audio(file_path: str) -> DetectorResult:
    """Model seam for the future CNN + LSTM audio detector."""
    return DetectorResult("FAKE", 91.2, "completed", "Mock audio detection completed; model integration is pending.")
