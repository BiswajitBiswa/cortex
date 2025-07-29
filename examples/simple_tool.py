# yamcp/plugins/examples/simple_tool.py
from logics.core.decorators import tool


@tool("say_hello")
def say_hello(name: str):
    return f"Hello, {name}!"
