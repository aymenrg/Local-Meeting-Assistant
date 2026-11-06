import pytest
import time
from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.domain.speech_utterance import SpeechUtterance
from src.agent_x.application.dto.requests import ManualQueryRequest, UIUpdateViewModel
from src.agent_x.application.ports.interfaces import IScreenScanner, IReasoningEngine, ISummaryPresenter
from src.agent_x.application.use_cases.process_screen_scan import ProcessScreenScanUseCase
from src.agent_x.application.use_cases.generate_contextual_answer import GenerateContextualAnswerUseCase

class MockScanner(IScreenScanner):
    async def capture_visible_context(self) -> str:
        return "Competitor Pricing Table"

class MockReasoningEngine(IReasoningEngine):
    async def generate_insight(self, prompt: str) -> str:
        return "Suggest focusing on our superior SLA."

class MockPresenter(ISummaryPresenter):
    def __init__(self):
        self.last_rendered_view: UIUpdateViewModel = None
        
    def display_summary(self, view_model: UIUpdateViewModel) -> None:
        self.last_rendered_view = view_model

@pytest.mark.asyncio
async def test_process_screen_scan_updates_memory():
    memory = SessionMemory()
    use_case = ProcessScreenScanUseCase(memory, MockScanner())
    await use_case.execute()
    
    assert memory.current_visual is not None
    assert memory.current_visual.extracted_text == "Competitor Pricing Table"

@pytest.mark.asyncio
async def test_generate_answer_orchestrates_correctly():
    memory = SessionMemory()
    memory.add_utterance(SpeechUtterance("Client says they need it cheaper.", time.time()))
    
    presenter = MockPresenter()
    use_case = GenerateContextualAnswerUseCase(memory, MockReasoningEngine(), presenter)
    
    request = ManualQueryRequest(query="How do I respond?", timestamp=time.time())
    await use_case.execute(request)
    
    assert presenter.last_rendered_view is not None
    assert presenter.last_rendered_view.formatted_summary == "Suggest focusing on our superior SLA."
    assert presenter.last_rendered_view.system_status == "active"
