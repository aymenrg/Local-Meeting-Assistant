import time
from src.agent_x.domain.session_memory import SessionMemory
from src.agent_x.domain.speech_utterance import SpeechUtterance
from src.agent_x.domain.visual_snapshot import VisualSnapshot

def test_add_utterance_updates_token_count():
    memory = SessionMemory(max_token_limit=1000)
    # "Hello world" is 11 chars -> ~2 tokens
    utterance = SpeechUtterance(text="Hello world", timestamp=time.time())
    memory.add_utterance(utterance)
    
    assert len(memory.utterances) == 1
    assert memory._current_token_count > 0

def test_lru_token_eviction_drops_oldest_data():
    # Set a tiny limit of 5 tokens
    memory = SessionMemory(max_token_limit=5)
    
    # 20 chars = 5 tokens
    u1 = SpeechUtterance(text="A"*20, timestamp=time.time()) 
    memory.add_utterance(u1)
    assert len(memory.utterances) == 1 # Fits perfectly
    
    # 20 chars = 5 tokens (this pushes the total to 10, exceeding the limit of 5)
    u2 = SpeechUtterance(text="B"*20, timestamp=time.time())
    memory.add_utterance(u2)
    
    # The memory should have dropped u1 to make room for u2
    assert len(memory.utterances) == 1
    assert memory.utterances[0].text == "B"*20

def test_privacy_purge_destroys_all_data():
    memory = SessionMemory()
    memory.add_utterance(SpeechUtterance(text="Secret meeting data", timestamp=time.time()))
    memory.set_visual_snapshot(VisualSnapshot(extracted_text="Confidential slide", timestamp=time.time()))
    
    # Execute the privacy rule
    memory.purge()
    
    assert len(memory.utterances) == 0
    assert memory.current_visual is None
    assert memory._current_token_count == 0
