# from yamcp.base_server import BaseServer
from yamcp.config import config
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins


class EmbedServer(CoreApp):
    def __init__(self, plugin_paths):
        super().__init__(plugin_paths)
        # self.plugin_paths = plugin_paths
        # self.core_app = CoreApp()
        # self.plugin_paths = config.YAMCP_PLUGIN_PATHS
        # register_plugins(self.core_app, self.plugin_paths)

    @staticmethod
    def run():
        print("Use `runner = EmbeddedRunner(...)` in your Python code.")
