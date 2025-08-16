import httpx
from a2a.core.message import AgentMessage


class HTTPMessenger:
    def __init__(self, agent_registry: dict):
        """
        agent_registry: Dict of agent_id → agent_url (e.g., {"agent_b": "http://localhost:9002/a2a/receive"})
        """
        self.agent_registry = agent_registry

    async def send(self, message: AgentMessage):
        if message.receiver not in self.agent_registry:
            raise ValueError(f"Unknown agent: {message.receiver}")

        url = self.agent_registry[message.receiver]

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=message.dict())
            response.raise_for_status()
            return response.json()  # Optional: if agent replies inline

    async def broadcast(self, message: AgentMessage):
        for agent_id, url in self.agent_registry.items():
            if agent_id != message.sender:  # skip sender if needed
                await self.send(AgentMessage(**{
                    **message.dict(),
                    "receiver": agent_id
                }))
