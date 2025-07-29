import asyncio
import httpx

API_BASE = "http://localhost:8080/api/http/run"


async def call_tool(tool_name: str, params: dict):
    url = f"{API_BASE}/{tool_name}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            return data["result"]
        else:
            raise Exception(f"Tool error: {data}")


async def main():
    # Call say_hello tool
    greeting = await call_tool("say_hello", {"name": "Alice"})
    print("say_hello result:", greeting)

    # Call reverse_text tool (async class-based tool)
    reversed_str = await call_tool("reverse_text", {"text": "YAMCP"})
    print("reverse_text result:", reversed_str)

    # Call greet (router plugin tool)
    greet_result = await call_tool("greet", {"name": "Bob"})
    print("greet result:", greet_result)


if __name__ == "__main__":
    asyncio.run(main())
