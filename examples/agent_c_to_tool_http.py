import uvicorn
from fastapi import FastAPI
from yamcp.core.app import CoreApp
from a2a.core.message import AgentMessage
from yamcp.core.app import CoreApp

# Import tool setup to ensure registration

app = FastAPI()
app.mount("/api", app)


@app.post("/a2a/receive")
async def receive_msg(msg: AgentMessage):
    print(f"[agent_b] Got message from {msg.sender}: {msg.payload}")

    result = await CoreApp().dispatch("say_hello", **msg.payload)

    return {
        "status": "ok",
        "reply_to": msg.task,
        "result": result,
    }


uvicorn.run(app, host="0.0.0.0", port=9003)
