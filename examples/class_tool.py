# yamcp/plugins/examples/class_tool.py
from logics.core.decorators import ToolBase
from logics.transport.grpc_server import core_app


class ReverseText(ToolBase):
    name = "reverse_text"
    description = "Reverses a string"
    author = "dev"

    async def run(self, text: str):
        return text[::-1]

# core_app.register_tool("greet1", ReverseText)