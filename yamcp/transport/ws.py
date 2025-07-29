# yamcp/transport/ws.py
from fastapi import FastAPI, WebSocket, APIRouter
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class WebSocketServer:
    def __init__(self, core_app: CoreApp):
        # self.app = FastAPI(title="YAMCP WebSocket Server")
        self.core_app = core_app
        # register_plugins(self.core_app, plugin_paths)
        self.router = APIRouter()
        self.setup_routes()
        # self.app.include_router(self.router, prefix="/api")
        self.setup_websocket()

    def setup_routes(self):
        @self.router.get("/tools")
        def list_tools():
            return {"tools": self.core_app.list_tools()}

    def setup_websocket(self):
        @self.router.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_json()
                    tool = data.get("tool")
                    args = data.get("args", {})
                    result = await self.core_app.dispatch(tool, args)
                    if hasattr(result, "__aiter__"):
                        async for item in result:
                            await websocket.send_json({"stream": item})
                    else:
                        await websocket.send_json({"result": result})
            finally:
                await websocket.close()
