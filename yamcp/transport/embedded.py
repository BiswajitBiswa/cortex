# yamcp/transport/embedded.py
import asyncio
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class EmbeddedRunner:
    def __init__(self, core_app: CoreApp):
        self.core_app = core_app

    async def run(self, tool: str, args: dict):
        return await self.core_app.dispatch(tool, args)
