# yamcp/tests/test_core.py
import pytest
from yamcp.core.app import CoreApp
from yamcp.plugins.examples.simple_tool import say_hello

@pytest.mark.asyncio
async def test_hello():
    app = CoreApp()
    app.register_tool("say_hello", say_hello)
    result = await app.dispatch("say_hello", {"name": "Test"})
    assert result == "Hello, Test!"
