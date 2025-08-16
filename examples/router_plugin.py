# TODO: fix implicit register

from fastapi import APIRouter

from yamcp.core.app import CoreApp
from yamcp.core.decorators import ToolBase

router = APIRouter()


@router.get("/hello")
async def hello():
    return {"msg": "Hello from plugin"}


def run_tool_example(name: str) -> str:
    return f"Hello {name} from router plugin!"


def register(core_app: CoreApp, app=None):
    # Register a tool in core_app

    # core_app.register_tool(name="greet", tool=run_tool_example)
    # ToolBase().register(core_app=core_app)
    if app:
        app.include_router(router, prefix="/plugin")
