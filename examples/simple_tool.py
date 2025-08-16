# yamcp/plugins/examples/simple_tool.py
from yamcp.core.decorators import tool


@tool(name="say_hello", description="Says Hello To Given Name.", version="2.0.0")
def say_hello(name: str):
    return f"Hello, {name}!"
