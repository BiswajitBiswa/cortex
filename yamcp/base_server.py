# from yamcp.config import config
# from yamcp.core.app import CoreApp
# from yamcp.plugins.loader import register_plugins
#
#
# class BaseServer:
#     def __init__(self, plugin_paths=None):
#         self.plugin_paths = plugin_paths
#         self.core_app = CoreApp()
#         self.plugin_paths = config.YAMCP_PLUGIN_PATHS
#         register_plugins(self.core_app, self.plugin_paths)
#
#     def discover_tools(self):
#         return {"tools": self.core_app.list_tools()}
#
