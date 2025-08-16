import inspect
from typing import Callable, Optional, Dict, Any, get_type_hints

registered_tools: Dict[str, Callable] = {}
tool_metadata: Dict[str, Dict[str, Any]] = {}


def tool(name: Optional[str] = None, description: Optional[str] = None, version: Optional[str] = "0.1.0"):
    def decorator(func: Callable):
        tool_name = name or func.__name__

        sig = inspect.signature(func)
        param_types = {
            k: str(v.annotation.__name__) if v.annotation != inspect.Parameter.empty else "Any"
            for k, v in sig.parameters.items()
        }

        docstring = description or func.__doc__ or "No description provided."

        # Store metadata
        tool_metadata[tool_name] = {
            "type": "TOOL",
            "name": tool_name,
            "version": version,
            "description": docstring.strip(),
            "parameters": param_types,
        }

        setattr(func, "type", "TOOL")
        setattr(func, "name", tool_name)
        setattr(func, "description", docstring.strip())
        setattr(func, "version", version)
        setattr(func, "parameters", param_types)
        registered_tools[tool_name] = func

        return func

    return decorator


def is_tool(obj) -> bool:
    return getattr(obj, "type", None) == "TOOL"


class ToolBase:
    name: str = "unknown_tool"
    description: str = "No description provided"
    version: str = "0.1.0"

    async def run(self, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_tool_metadata(cls):
        # For function-based tools
        if callable(cls) and hasattr(cls, "parameters"):
            return {
                "type": getattr(cls, "type", "TOOL"),
                "name": getattr(cls, "name", cls.__name__),
                "description": getattr(cls, "description", "No description provided."),
                "version": getattr(cls, "version", "0.1.0"),
                "parameters": getattr(cls, "parameters", {}),
            }
        # For class-based tools (ToolBase subclasses)
        elif isinstance(cls, type) and issubclass(cls, ToolBase):
            return cls.metadata()
        elif isinstance(cls, ToolBase):
            return cls.metadata()
        else:
            return {}

    @classmethod
    def metadata(cls) -> Dict[str, Any]:
        try:
            run_method = getattr(cls, "run", None)
            if run_method is None:
                params = {}
            else:
                sig = inspect.signature(run_method)
                # skip 'self'
                params = {
                    k: (v.annotation.__name__ if v.annotation != inspect.Parameter.empty else "Any")
                    for k, v in sig.parameters.items() if k != "self"
                }
        except Exception as e:
            params = {}

        return {
            "type": "TOOL",
            "name": getattr(cls, "name", "unknown_tool"),
            "description": getattr(cls, "description", "No description provided"),
            "author": getattr(cls, "author", "anonymous"),
            "version": getattr(cls, "version", "0.1.0"),
            "parameters": params,
        }

    @classmethod
    def register(cls, core_app, app=None):
        instance = cls()
        core_app.register_tool(cls.name, instance)
