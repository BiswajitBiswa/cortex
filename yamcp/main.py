import argparse
import os
import uvicorn

from yamcp.config import config
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins

from yamcp.http_ws_server import HTTPWSServer
from yamcp.cli_server import CLIServer
from yamcp.embed_server import EmbedServer


class MainRunner:
    def __init__(self):
        self.args = self.parse_args()

        self.mode = self.args.mode or os.getenv("YAMCP_MODE", config.YAMCP_MODE)
        self.plugin_paths = self.args.plugins.split(",") if self.args.plugins else config.YAMCP_PLUGIN_PATHS

        self.host = self.args.host or os.getenv("YAMCP_HOST", config.YAMCP_HOST)
        self.port = self.args.port or int(os.getenv("YAMCP_PORT", config.YAMCP_PORT))


        # Set into env for reload-compatible access
        # os.environ["YAMCP_MODE"] = self.mode
        # os.environ["YAMCP_PLUGIN_PATHS"] = ",".join(self.plugin_paths)
        # os.environ["YAMCP_HOST"] = self.host
        # os.environ["YAMCP_PORT"] = str(self.port)

        # Create CoreApp and register plugins ONCE here
        self.core_app = CoreApp()
        register_plugins(self.core_app, self.plugin_paths)

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Run YAMCP in different modes.")
        parser.add_argument("--mode", choices=["cli", "httpws", "embed"], help="Mode to run the server in")
        parser.add_argument("--plugins", help="Comma-separated plugin paths")
        parser.add_argument("--host", help="Server host")
        parser.add_argument("--port", type=int, help="Server port")
        return parser.parse_args()

    def run(self):
        if self.mode == "cli":
            server = CLIServer(self.plugin_paths)
            server.run()

        elif self.mode in ["http", "ws", "http_ws"]:
            server = HTTPWSServer()
            server.run()

        elif self.mode == "embed":
            server = EmbedServer()
            server.run()

        else:
            raise ValueError(f"Unknown mode: {self.mode}")


if __name__ == "__main__":
    MainRunner().run()
