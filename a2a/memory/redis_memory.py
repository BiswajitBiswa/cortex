# a2a/memory/redis_memory.py
from typing import Dict, Any

import aioredis
import json
from a2a.memory.base_memory import BaseMemoryStore


class RedisMemoryStore(BaseMemoryStore):
    def __init__(self, redis_url="redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def save_context(self, agent_id: str, context: Dict[str, Any]):
        await self.redis.set(f"context:{agent_id}", json.dumps(context))

    async def get_context(self, agent_id: str) -> Dict[str, Any]:
        data = await self.redis.get(f"context:{agent_id}")
        if data:
            return json.loads(data)
        return {}
