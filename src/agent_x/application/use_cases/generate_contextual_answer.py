from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.application.ports.interfaces import IReasoningEngine, ISummaryPresenter
from src.agent_x.application.dto.requests import ManualQueryRequest, UIUpdateViewModel

class GenerateContextualAnswerUseCase:
    def __init__(self, 
                 memory: SessionMemory, 
                 reasoning_engine: IReasoningEngine, 
                 presenter: ISummaryPresenter):
        self.memory = memory
        self.reasoning_engine = reasoning_engine
        self.presenter = presenter

    async def execute(self, request: ManualQueryRequest) -> None:
        """Merges memory contexts, queries the LLM, and updates the UI."""
        audio_context = "\n".join([u.text for u in self.memory.utterances])
        visual_context = self.memory.current_visual.extracted_text if self.memory.current_visual else "No visual data."
        
        prompt = f"""
        System: You are an elite sales assistant. Be concise. 
        Recent Audio Transcript: {audio_context}
        Visible Screen Data: {visual_context}
        User Question: {request.query}
        Response:
        """

        try:
            raw_response = await self.reasoning_engine.generate_insight(prompt)
            status = "active"
        except Exception as e:
            raw_response = "System warning: Local inference offline. Attempting automatic restart."
            status = "degraded"

        view_model = UIUpdateViewModel(formatted_summary=raw_response, system_status=status)
        self.presenter.display_summary(view_model)
