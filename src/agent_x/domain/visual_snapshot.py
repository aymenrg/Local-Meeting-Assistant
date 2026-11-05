from dataclasses import dataclass

@dataclass
class VisualSnapshot:
    extracted_text: str
    timestamp: float
    
    @property
    def estimated_tokens(self) -> int:
        return max(1, len(self.extracted_text) // 4)
