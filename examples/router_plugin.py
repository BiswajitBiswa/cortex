# myplugin.py
from fastapi import APIRouter

from logics.core.app import CoreApp

router = APIRouter()


@router.get("/hello")
async def hello():
    return {"msg": "Hello from plugin"}


def run_tool_example(name: str) -> str:
    return f"Hello {name} from router plugin!"


def register(core_app: CoreApp, app=None):
    # Register a tool in core_app
    core_app.register_tool("greet", run_tool_example)

    # If FastAPI app is provided, include the plugin router
    if app:
        app.include_router(router, prefix="/plugin")
