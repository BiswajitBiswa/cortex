# yamcp/transport/http.py
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import create_model
import inspect
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class HTTPServer:
    def __init__(self, core_app: CoreApp):
        self.core_app = core_app
        # register_plugins(self.core_app, plugin_paths, self.app)
        self.router = APIRouter()
        self.register_routes()
        # self.app.include_router(self.router, prefix="/http")

    def register_routes(self):
        @self.router.get("/tools")
        def list_tools():
            return {"tools": self.core_app.list_tools()}

        @self.router.post("/run/{tool_name}")
        async def run_tool(tool_name: str, body: dict):
            tool = self.core_app.tools.get(tool_name)
            if not tool:
                raise HTTPException(404, f"Tool '{tool_name}' not found")
            model = self.make_tool_request_model(tool_name, tool)
            payload = model(**body)
            result = await self.core_app.dispatch(tool_name, payload.dict())
            return {"status": "ok", "result": result}

    @staticmethod
    def make_tool_request_model(tool_name: str, func):
        sig = inspect.signature(func.run if hasattr(func, "run") else func)
        fields = {name: (param.annotation or (str,), ...) for name, param in sig.parameters.items()}
        return create_model(f"{tool_name}_Model", **fields)

