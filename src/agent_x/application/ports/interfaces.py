from abc import ABC, abstractmethod
from src.agent_x.application.dto.requests import UIUpdateViewModel

class IScreenScanner(ABC):
    @abstractmethod
    async def capture_visible_context(self) -> str:
        """Takes a snapshot of the Wayland display and extracts text via OCR."""
        pass

class IReasoningEngine(ABC):
    @abstractmethod
    async def generate_insight(self, prompt: str) -> str:
        """Sends the structured prompt to the local LLM and returns the generated text."""
        pass

class ISummaryPresenter(ABC):
    @abstractmethod
    def display_summary(self, view_model: UIUpdateViewModel) -> None:
        """Pushes the generated AI response to the PyQt UI overlay."""
        pass
