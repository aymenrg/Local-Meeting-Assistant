import time
import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.domain.speech_utterance import SpeechUtterance
from src.agent_x.infrastructure.audio_capture import PipeWireAudioCapture
from src.agent_x.infrastructure.whisper_engine import WhisperEngine

class ContinuousAudioWorker(QThread):
    """Runs in the background to feed live audio into the session memory."""
    
    def __init__(self, memory: SessionMemory):
        super().__init__()
        self.memory = memory
        self.capture = PipeWireAudioCapture()
        self.transcriber = WhisperEngine(model_size="base")
        self.is_running = True

    def run(self):
        """The continuous listening loop."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while self.is_running:
            # 1. Record chunk
            wav_path = self.capture.record_chunk()
            
            # 2. Transcribe
            text = loop.run_until_complete(self.transcriber.transcribe_audio_chunk(wav_path))
            
            # 3. Save to memory if speech was detected
            if text:
                print(f"[Memory Added]: {text}")
                utterance = SpeechUtterance(text=text, timestamp=time.time())
                self.memory.add_utterance(utterance)
