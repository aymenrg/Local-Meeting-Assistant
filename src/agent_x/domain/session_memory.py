from typing import List, Optional
from src.agent_x.domain.speech_utterance import SpeechUtterance
from src.agent_x.domain.visual_snapshot import VisualSnapshot

class SessionMemory:
    def __init__(self, max_token_limit: int = 3000):
        self.max_token_limit = max_token_limit
        self.utterances: List[SpeechUtterance] = []
        self.current_visual: Optional[VisualSnapshot] = None
        self._current_token_count = 0

    def add_utterance(self, utterance: SpeechUtterance) -> None:
        """Injects new speech and enforces the LRU token limit to prevent GPU crashes."""
        self.utterances.append(utterance)
        self._current_token_count += utterance.estimated_tokens
        self._enforce_lru_token_limit()

    def set_visual_snapshot(self, snapshot: VisualSnapshot) -> None:
        """Overwrites the previous snapshot. We only ever care about the newest scan."""
        if self.current_visual:
            self._current_token_count -= self.current_visual.estimated_tokens
            
        self.current_visual = snapshot
        self._current_token_count += snapshot.estimated_tokens
        self._enforce_lru_token_limit()

    def _enforce_lru_token_limit(self) -> None:
        """Drops the oldest utterances if the total context exceeds the safe limit."""
        while self._current_token_count > self.max_token_limit and self.utterances:
            dropped = self.utterances.pop(0)
            self._current_token_count -= dropped.estimated_tokens

    def purge(self) -> None:
        """
        [CRITICAL PRIVACY RULE]: Instantly nullifies all stored data in RAM.
        This must be called when the meeting ends or the UI closes.
        """
        self.utterances.clear()
        self.current_visual = None
        self._current_token_count = 0
