from dataclasses import dataclass
import time

@dataclass
class SpeechUtterance:
    text: str
    timestamp: float
    
    @property
    def estimated_tokens(self) -> int:
        """Rough heuristic: 1 token is roughly 4 characters in English."""
        return max(1, len(self.text) // 4)

    def is_stale(self, max_age_seconds: int = 180) -> bool:
        """Returns True if the utterance is older than max_age_seconds (3 minutes)."""
        return (time.time() - self.timestamp) > max_age_seconds
