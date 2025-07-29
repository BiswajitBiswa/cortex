# logics/core/decorators.py
from typing import Callable, Optional, Dict


registered_tools: Dict[str, Callable] = {}

def tool(name: Optional[str] = None):
    def decorator(func: Callable):
        tool_name = name or func.__name__

        setattr(func, "_is_tool", True)
        setattr(func, "_tool_name", name or tool_name)
        registered_tools[tool_name] = func
        return func
    return decorator


def is_tool(obj) -> bool:
    return getattr(obj, "_is_tool", False)


# logics/core/decorators.py

class ToolBase:
    name: str
    # description: str = ""
    # version: str = "0.1.0"
    # author: str = "anonymous"

    # _registry = {}

    async def run(self, **kwargs):
        raise NotImplementedError

    @classmethod
    def register(cls, core_app, app=None):
        instance = cls()
        core_app.register_tool(cls.name, instance)