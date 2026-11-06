from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent_x.infrastructure.ollama_engine import OllamaReasoningEngine

app = FastAPI(title="Agent-X Local API")
engine = OllamaReasoningEngine(model_name="llama3") # Assuming llama3 is pulled locally

class PromptRequest(BaseModel):
    query: str

@app.post("/test-llm")
async def test_local_llm(request: PromptRequest):
    """Temporary endpoint for the client to test inference speed."""
    try:
        response = await engine.generate_insight(request.query)
        return {"local_response": response}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
