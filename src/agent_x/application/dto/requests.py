from pydantic import BaseModel, Field

class ManualQueryRequest(BaseModel):
    """The data object representing a typed user question."""
    query: str
    timestamp: float

class UIUpdateViewModel(BaseModel):
    """The pure data object passed to the UI layer for rendering."""
    formatted_summary: str
    system_status: str = "active"
