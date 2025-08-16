# a2a/memory/base_memory.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseMemoryStore(ABC):
    @abstractmethod
    async def save_context(self, agent_id: str, context: Dict[str, Any]): ...

    @abstractmethod
    async def get_context(self, agent_id: str) -> Dict[str, Any]: ...
