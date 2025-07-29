# yamcp/transport/stdio.py
import sys
import json
import asyncio
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class CLI:
    def __init__(self, plugin_paths):
        self.app = CoreApp()
        register_plugins(self.app, plugin_paths)

    async def run(self):
        print("YAMCP CLI Ready")
        while True:
            line = await asyncio.to_thread(sys.stdin.readline)
            if not line:
                break
            try:
                req = json.loads(line)
                result = await self.app.dispatch(req["tool"], req.get("args", {}))
                print(json.dumps({"result": result}))
            except Exception as e:
                print(json.dumps({"error": str(e)}))
