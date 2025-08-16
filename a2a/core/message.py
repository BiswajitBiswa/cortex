from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AgentMessage(BaseModel):
    sender: str  # agent_id
    receiver: str  # target agent_id
    type: str  # "task_request", "reply", "context_share"
    task: Optional[str] = Field(default=None) # optional task name or intent
    payload: Dict[str, Any]  # task-specific payload
    context: Optional[Dict[str, Any]] = Field(default=None)  # shared memory or previous outputs
    reply_to: Optional[str] = Field(default=None)  # task_id if response
