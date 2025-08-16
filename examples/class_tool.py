# yamcp/plugins/examples/class_tool.py
from yamcp.core.decorators import ToolBase
# from yamcp.transport.grpc_server import core_app


class ReverseText(ToolBase):
    name = "reverse_text"
    description = "Reverses a string"
    version = "1.0"

    async def run(self, text: str):
        return text[::-1]
# Registering
# ReverseText.register(core_app)

# core_app.register_tool("greet1", ReverseText)