from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent_x.infrastructure.ollama_engine import OllamaReasoningEngine
from src.agent_x.infrastructure.audio_capture import PipeWireAudioCapture
from src.agent_x.infrastructure.whisper_engine import WhisperEngine

audio_capture = PipeWireAudioCapture()
whisper_engine = WhisperEngine()

app = FastAPI(title="Agent-X Local API")
engine = OllamaReasoningEngine(model_name="llama3") # Assuming llama3 is pulled local


@app.post("/test-audio")
async def test_live_audio():
    """Records 5 seconds of audio from your mic and transcribes it locally."""
    try:
        # 1. Record the audio chunk
        temp_wav_path = audio_capture.record_chunk()
        
        # 2. Transcribe it offline
        text = await whisper_engine.transcribe_audio_chunk(temp_wav_path)
        
        if not text:
            return {"transcription": "[No speech detected]"}
        return {"transcription": text}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


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
