import httpx
from src.agent_x.application.ports.interfaces import IReasoningEngine

class OllamaReasoningEngine(IReasoningEngine):
    """Concrete implementation connecting to the local Ollama service."""
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    async def generate_insight(self, prompt: str) -> str:
        """Sends the prompt to the local LLM and returns the text response."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        # We use httpx.AsyncClient to ensure we don't freeze the Wayland UI
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                return response.json().get("response", "")
            except httpx.RequestError as e:
                raise RuntimeError(f"Failed to reach local Ollama: {e}")
