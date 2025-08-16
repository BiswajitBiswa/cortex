import asyncio
from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue

async def send_initial():
    queue = RedisQueue()
    msg = AgentMessage(
        sender="user",
        receiver="agent_a",
        type="task_request",
        task="process_text",
        payload={"text": "hello world"}
    )
    await queue.send(msg)
    print("Sent initial message to agent_a")

asyncio.run(send_initial())
