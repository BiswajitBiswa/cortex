from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue


async def agent_loop(agent_id: str):
    queue = RedisQueue()

    while True:
        msg = await queue.receive(agent_id)
        print(f"[{agent_id}] Received message from {msg.sender}: {msg.payload}")

        # Example: Echo back
        if msg.type == "task_request":
            reply = AgentMessage(
                sender=agent_id,
                receiver=msg.sender,
                type="reply",
                task=msg.task,
                payload={"result": f"Task '{msg.task}' completed."},
                reply_to=msg.task
            )
            await queue.send(reply)
