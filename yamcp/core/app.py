import inspect
from typing import Any, Callable, Dict, Union

from yamcp.config import config
from yamcp.core.decorators import ToolBase, is_tool
from yamcp.plugins.loader import register_plugins


class CoreApp:
    def __init__(self, plugin_paths=None):
        self.plugin_paths = plugin_paths or config.YAMCP_PLUGIN_PATHS
        # self.core_app = CoreApp()
        self.tools: Dict[str, Union[Callable, ToolBase]] = {}
        register_plugins(self.tools, self.plugin_paths)

    def register_tool(self, name: str, tool: Union[Callable, ToolBase]):
        # tool.__setattr__("name", "hey")
        self.tools[name] = tool

    def list_tools(self):
        return self.tools

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
