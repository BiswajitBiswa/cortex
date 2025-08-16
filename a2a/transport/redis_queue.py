import aioredis
import json

from a2a.core.message import AgentMessage
from a2a.core.queue_base import BaseMessageQueue


class RedisQueue(BaseMessageQueue):
    def __init__(self, redis_url="redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def send(self, message: AgentMessage):
        queue = f"a2a:{message.receiver}"
        await self.redis.rpush(queue, message.json())

    async def receive(self, agent_id: str) -> AgentMessage:
        queue = f"a2a:{agent_id}"
        _, raw_msg = await self.redis.blpop(queue)
        return AgentMessage.parse_raw(raw_msg)
