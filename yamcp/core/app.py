import inspect
from typing import Any, Callable, Dict, Union

from yamcp.core.decorators import ToolBase, is_tool


class CoreApp:
    def __init__(self):
        self.tools: Dict[str, Union[Callable, ToolBase]] = {}

    def register_tool(self, name: str, tool: Union[Callable, ToolBase]):
        self.tools[name] = tool

    def list_tools(self):
        return list(self.tools.keys())

    async def dispatch(self, tool_name: str, args: Dict[str, Any]) -> Any:
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not registered.")
        func = tool.run if isinstance(tool, ToolBase) else tool
        result = func(**args)
        if inspect.isasyncgen(result):
            return result
        elif inspect.iscoroutine(result):
            return await result
        else:
            return result
