import sounddevice as sd
import numpy as np
import tempfile
import wave
import os

class PipeWireAudioCapture:
    """Captures audio chunks from Ubuntu's default audio server."""
    
    def __init__(self, sample_rate: int = 16000, chunk_duration_sec: int = 5):
        self.sample_rate = sample_rate
        self.chunk_duration_sec = chunk_duration_sec

    def record_chunk(self) -> str:
        """Records a chunk and returns the path to a temporary WAV file."""
        print("Recording audio chunk...")
        recording = sd.rec(
            int(self.chunk_duration_sec * self.sample_rate), 
            samplerate=self.sample_rate, 
            channels=1, 
            dtype='int16'
        )
        sd.wait() # Block until the chunk is finished recording

        # Save temporarily for Whisper to process
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(recording.tobytes())
            
        return temp_file.name
