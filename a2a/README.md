# 🤖 A2A Messaging Module (Agent-to-Agent Communication)

Part of the **CORTEX/YAMCP** ecosystem by [Biswajit Tripathy](https://github.com/BiswajitBiswa), the **A2A** module enables scalable, memory-aware, and async-first communication between autonomous agents.

---

## 🧠 Goal of A2A Module

Enable **inter-agent communication** so agents can:

- Delegate tasks to other agents
- Share context/memory
- Coordinate workflows asynchronously or in real-time
- Support queue-based and/or direct messaging modes

---

## 🔧 Architecture Overview

### 1. Core Design Goals

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 🔌 Pluggable transport | Support for Redis, RabbitMQ, HTTP, WebSocket, or in-memory messaging        |
| 💬 Message schema      | Use standardized Pydantic-based schema for all agent communication          |
| 📚 Shared memory       | Optional memory stores (Redis, SQLite, vector DBs)                          |
| 🔄 Async support       | Async-safe queue + background task handling                                 |
| ⚙️ Routing logic        | Route by `agent_id`, `capability`, or `task`                                |
| 🧠 Memory-aware agents | Attach or retrieve shared context with messages                             |

---

## 📦 Examples: Agent-to-Agent Messaging in Action

Here are several runnable examples to test A2A messaging with both embedded tools and agent-to-agent communication using HTTP and Queue transports.

### 🧪 1. Agent B: Tool Handler via Embedded Mode

Start an embedded tool handler agent (Agent B):
```
python cortex/examples/agent_b_to_tool_embed.py
```
### 📡 2. Agent A: Sends Task to Agent B via HTTP

In a new terminal, run Agent A which sends a task to Agent B over HTTP:
```
python cortex/examples/agent_a_to_agent_b_http.py
```
### 🔁 3. Agent-to-Agent via Redis/In-Memory Queue
Step 1: Start Agent B Queue Listener
```
python cortex/examples/agent_b_loop.py
```
Step 2: Send Message from Agent A to Agent B
```
python cortex/examples/agent_a_to_agent_b_queue.py
```
### 🚀 4. Pre-seed Agent Queue with Initial Message

You can also test message queuing by sending a message directly to an agent's queue:
```
python cortex/examples/send_initial_msg_to_agentic_queue.py
```

## ✅ Prerequisites

Ensure the following before running the examples:

Python dependencies are installed 
```
pip install -r requirements.txt
```

Redis is running locally (for RedisQueue examples), or fallback to in-memory queue

.env is properly configured if needed for your queue/memory settings

🧠 What You’ll See

Agents sending tasks and receiving replies

Tool execution handled either by embedded mode or over HTTP

Queued message passing and response routing

Live logging of communication between agents

---

## 📬 AgentMessage Schema

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentMessage(BaseModel):
    sender: str
    receiver: str
    type: str  # "task_request", "reply", "context_share"
    task: Optional[str]
    payload: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    reply_to: Optional[str] = None
```

---

## 🔄 Queue Interface Design

### Abstract Queue

```python
class BaseMessageQueue:
    async def send(self, message: AgentMessage): ...
    async def receive(self, agent_id: str) -> AgentMessage: ...
    async def broadcast(self, message: AgentMessage): ...
```

### RedisQueue Example

```python
import aioredis
import json

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
```

---

## 🧠 Agent Memory Store

```python
class BaseMemoryStore:
    async def save_context(self, agent_id: str, context: Dict[str, Any]): ...
    async def get_context(self, agent_id: str) -> Dict[str, Any]: ...
```

---

## 🧪 Minimal Agent Runner

```python
from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue

async def agent_loop(agent_id: str):
    queue = RedisQueue()
    
    while True:
        msg = await queue.receive(agent_id)
        print(f"[{agent_id}] Received from {msg.sender}: {msg.payload}")

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
```

---

## 📨 Sending a Task

```python
# agent_a.py
from a2a.core.message import AgentMessage
from a2a.transport.redis_queue import RedisQueue

async def agent_a():
    queue = RedisQueue()
    msg = AgentMessage(
        sender="agent_a",
        receiver="agent_b",
        type="task_request",
        task="reverse_text",
        payload={"text": "YAMCP"}
    )
    await queue.send(msg)
```

---

## 🌐 HTTP Messenger Transport (Optional)

```python
import httpx
from a2a.core.message import AgentMessage

class HTTPMessenger:
    def __init__(self, agent_registry: dict):
        self.agent_registry = agent_registry

    async def send(self, message: AgentMessage):
        if message.receiver not in self.agent_registry:
            raise ValueError(f"Unknown agent: {message.receiver}")
        
        url = self.agent_registry[message.receiver]

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=message.dict())
            response.raise_for_status()
            return response.json()

    async def broadcast(self, message: AgentMessage):
        for agent_id, url in self.agent_registry.items():
            if agent_id != message.sender:
                await self.send(AgentMessage(**{
                    **message.dict(),
                    "receiver": agent_id
                }))
```

---

## 📥 FastAPI Receiver Example

```python
# agent_b_server.py

from fastapi import FastAPI
from a2a.core.message import AgentMessage

app = FastAPI()

@app.post("/a2a/receive")
async def receive_agent_message(msg: AgentMessage):
    print(f"Received from {msg.sender}: {msg.payload}")

    if msg.type == "task_request":
        result = {"result": msg.payload["text"][::-1]}
        return {
            "status": "ok",
            "reply_to": msg.task,
            "result": result
        }

    return {"status": "ok"}
```

---

## 🔁 A2A vs YAMCP Tool Invocation

| Feature                      | YAMCP Tool (HTTP Call)         | A2A Messaging                      |
|------------------------------|--------------------------------|------------------------------------|
| 🎯 Purpose                   | Stateless tool execution       | Agent coordination & delegation    |
| 🔁 Flow                      | One-shot                       | Async message + optional reply     |
| 🧠 Context Support           | No                             | Yes (via memory/context)           |
| 📡 Protocol                  | REST/WS CLI                    | JSON schema over Redis/HTTP/etc    |
| 📬 Delegation / Forwarding   | Manual                         | Built-in                           |
| 🧵 Async Compatible          | Not inherently                 | Yes                                |
| 🗂️ Agent Lifecycle           | Stateless                      | Long-lived / memory-aware          |

---

## 🧠 Integration with YAMCP

Agents using tools can also delegate tasks to other agents via A2A:

```python
@tool("delegate_to_agent_b")
async def delegate_tool(text: str):
    msg = AgentMessage(
        sender="tool_agent",
        receiver="agent_b",
        type="task_request",
        task="reverse_text",
        payload={"text": text}
    )
    await queue.send(msg)
```

---

## 🗺️ Roadmap

| Feature                          | Status        |
|----------------------------------|---------------|
| ✅ Redis/In-memory messaging      | ✅ v0.1 Ready |
| 🔄 Reply/callback chaining        | In design     |
| 🧠 Memory sharing between agents  | Optional      |
| ⛓️ Message middleware/logging     | Planned       |
| 🌐 HTTP/Webhook transport         | ✅ Available  |
| 🧩 LangChain Tool Adapter         | Planned       |
| 🔍 Agent registry/discovery       | Planned       |

---

## 🤝 Contributing

We welcome:

- 🚀 New transports (MQTT, WebSocket, gRPC)
- 🧠 Memory plugins (vector DB, token window)
- 🧩 Adapters (LangChain, Semantic Kernel)
- 🧪 Test scenarios and benchmarks

> Open an issue or PR at: [github.com/BiswajitBiswa](https://github.com/BiswajitBiswa)

---

## 🔗 Related Projects

- 🧠 [CORTEX README](https://github.com/BiswajitBiswa/cortex)
- 🛠️ [YAMCP Tool Server](https://github.com/BiswajitBiswa/yamcp)
- 💬 A2A Messaging Module (This README)

---

## ✨ Vision

> “Agents that collaborate. Tools that coordinate. Contexts that persist.”

🎯 Build smarter. Communicate asynchronously. Orchestrate at scale.

---

© 2025 — A2A Module by **Biswajit Tripathy** — [GitHub](https://github.com/BiswajitBiswa)
