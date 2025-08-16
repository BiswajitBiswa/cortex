# import typer
# import asyncio
# from rich import print
#
# from yamcp.config import config
# from yamcp.core.app import CoreApp
# from yamcp.plugins.loader import register_plugins
# from yamcp.core.decorators import ToolBase
# from yamcp.core.app import CoreApp
# from yamcp.cli_server import CLIServer
#
# typer_app = typer.Typer(no_args_is_help=True)
#
#
# class CLI:
#     def __init__(self, core_app: CoreApp):
#         self.core_app = core_app
#
#     async def run(self, tool: str, args: dict):
#         return await self.core_app.dispatch(tool, args)
#
# cli = CLI()
# @typer_app.command()
# def list():
#     """List all available tools"""
#     print("[bold cyan]Available tools:[/bold cyan]")
#     for name, tool in core_app.tools.items():
#         try:
#             meta = tool.metadata()
#         except Exception as e:
#             meta = {"description": "Failed to load metadata", "parameters": {}}
#
#         params = ", ".join(f"{k}: {v}" for k, v in meta.get("parameters", {}).items())
#         print(f"  - [bold green]{name}[/bold green]({params})  — {meta.get('description', '')}")
#
#
# @typer_app.command()
# def run(tool: str, args: str = typer.Argument(None, help="JSON string of arguments")):
#     """Run a tool with given args"""
#     import json
#
#     try:
#         parsed_args = json.loads(args) if args else {}
#     except json.JSONDecodeError:
#         print("[red]Invalid JSON in args[/red]")
#         raise typer.Exit(code=1)
#
#     async def dispatch():
#         result = await core_app.dispatch(tool, parsed_args)
#         print(f"[green]Result:[/green] {result}")
#
#     asyncio.run(dispatch())
#
#
# @typer_app.command()
# def info(tool: str):
#     """Show metadata for a tool"""
#     tool_obj = core_app.tools.get(tool)
#     if not tool_obj:
#         print(f"[red]Tool '{tool}' not found.[/red]")
#         raise typer.Exit(code=1)
#
#     meta = tool_obj.metadata()
#
#     print("[bold cyan]Tool Metadata:[/bold cyan]")
#     for key, val in meta.items():
#         print(f"[yellow]{key}[/yellow]: {val}")
