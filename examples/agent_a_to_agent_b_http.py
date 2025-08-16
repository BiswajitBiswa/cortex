import asyncio

from a2a.core.message import AgentMessage
from a2a.transport.http_messenger import HTTPMessenger

async def main():
    agent_registry = {
        "agent_b": "http://0.0.0.0:9003/api/a2a/receive"
    }

    messenger = HTTPMessenger(agent_registry)

    msg = AgentMessage(
        sender="agent_a",
        receiver="agent_b",
        type="task_request",
        task="say_hello",
        payload={"name": "A2A"}
    )

    reply = await messenger.send(msg)
    print("Got reply from agent_b:", reply)


if __name__ == "__main__":
    asyncio.run(main())
