from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class DetectorResult:
    prediction: Literal["REAL", "FAKE"]
    confidence: float
    status: Literal["completed", "failed"]
    summary: str
