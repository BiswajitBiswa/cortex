# yamcp/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.YAMCP_MODE = os.getenv("YAMCP_MODE", "cli")
        self.YAMCP_PLUGIN_PATHS = self._parse_paths(os.getenv("YAMCP_PLUGINS", "yamcp/plugins/examples/simple_tool.py"))
        self.YAMCP_HOST = os.getenv("YAMCP_HOST", "0.0.0.0")
        self.YAMCP_PORT = int(os.getenv("YAMCP_PORT", 8000))

    @staticmethod
    def _parse_paths(paths: str):
        return [p.strip() for p in paths.split(",") if p.strip()]


config = Config()
