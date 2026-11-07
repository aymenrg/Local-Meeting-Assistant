import os
from faster_whisper import WhisperModel
from src.agent_x.application.ports.interfaces import IAudioTranscriber

class WhisperEngine(IAudioTranscriber):
    """Local offline transcription using faster-whisper."""
    
    def __init__(self, model_size: str = "tiny.en"):
        # "tiny.en" is incredibly fast on CPU and perfectly sufficient for meetings
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    async def transcribe_audio_chunk(self, file_path: str) -> str:
        """Transcribes the audio and instantly deletes the file for privacy."""
        try:
            segments, info = self.model.transcribe(file_path, beam_size=5)
            transcription = " ".join([segment.text for segment in segments])
            return transcription.strip()
        finally:
            # [PRIVACY RULE]: Purge the physical audio file immediately after processing
            if os.path.exists(file_path):
                os.remove(file_path)
