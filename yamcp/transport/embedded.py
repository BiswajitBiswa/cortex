# yamcp/transport/embedded.py
import asyncio
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class EmbeddedRunner:
    def __init__(self, plugin_paths):
        self.app = CoreApp()
        register_plugins(self.app, plugin_paths)

    async def run(self, tool: str, args: dict):
        return await self.app.dispatch(tool, args)
