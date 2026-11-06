import time
from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.domain.visual_snapshot import VisualSnapshot
from src.agent_x.application.ports.interfaces import IScreenScanner

class ProcessScreenScanUseCase:
    def __init__(self, memory: SessionMemory, scanner: IScreenScanner):
        self.memory = memory
        self.scanner = scanner

    async def execute(self) -> None:
        """Captures the screen and updates the short-term memory."""
        try:
            extracted_text = await self.scanner.capture_visible_context()
            snapshot = VisualSnapshot(extracted_text=extracted_text, timestamp=time.time())
            self.memory.set_visual_snapshot(snapshot)
        except Exception as e:
            print(f"Warning: Screen capture degraded or failed: {e}")
