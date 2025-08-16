import asyncio
import json

from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue

async def agent_a_loop():
    queue = RedisQueue()
    agent_id = "agent_a"

    # Simulate receiving a message to delegate task
    while True:
        msg = await queue.receive(agent_id)
        print(f"[Agent A] Received from {msg.sender}: {msg.payload}")

        if msg.type == "task_request" and msg.task == "process_text":
            # Delegate to Agent B to reverse the text
            delegate_msg = AgentMessage(
                sender=agent_id,
                receiver="agent_b",
                type="task_request",
                task="reverse_text",
                payload=msg.payload,
                reply_to=msg.task
            )
            await queue.send(delegate_msg)
            print("[Agent A] Delegated reverse_text task to Agent B.")

        elif msg.type == "reply" and msg.reply_to == "process_text":
            reversed_text = msg.payload.get("reversed")
            print(f"[Agent A] Got reversed text from Agent B: {reversed_text}")

            # Call local YAMCP tool to uppercase it (simulated here)
            uppercased = reversed_text.upper()
            print(f"[Agent A] Processed final result: {uppercased}")

            # Reply back to original sender if needed (omitted for brevity)

asyncio.run(agent_a_loop())
