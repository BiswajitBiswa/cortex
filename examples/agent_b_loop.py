import asyncio
from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue


async def agent_b_loop():
    queue = RedisQueue()
    agent_id = "agent_b"

    while True:
        msg = await queue.receive(agent_id)
        print(f"[Agent B] Received from {msg.sender}: {msg.payload}")

        if msg.type == "task_request" and msg.task == "reverse_text":
            text = msg.payload.get("text", "")
            reversed_text = text[::-1]

            reply_msg = AgentMessage(
                sender=agent_id,
                receiver=msg.sender,
                type="reply",
                task="reverse_text",
                payload={"reversed": reversed_text},
                reply_to=msg.task
            )
            await queue.send(reply_msg)
            print(f"[Agent B] Sent reversed text back to {msg.sender}")


asyncio.run(agent_b_loop())
