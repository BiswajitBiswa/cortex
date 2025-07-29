import asyncio
from yamcp.transport.stdio import CLI


class CLIServer:
    def __init__(self, plugin_paths):
        self.plugin_paths = plugin_paths

    def run(self):
        asyncio.run(CLI(self.plugin_paths).run())
