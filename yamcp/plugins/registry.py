# # yamcp/plugins/registry.py
# import importlib.util
# import os
# from yamcp.core.decorators import is_tool, ToolBase
#
#
# def register_plugins(core_app):
#     from yamcp.plugins.examples import simple_tool, class_tool
#
#     for mod in [simple_tool, class_tool]:
#         for attr in dir(mod):
#             obj = getattr(mod, attr)
#             if is_tool(obj):
#                 core_app.register_tool(getattr(obj, "_tool_name"), obj)
#             elif isinstance(obj, type) and issubclass(obj, ToolBase):
#                 instance = obj()
#                 core_app.register_tool(instance.name, instance)
