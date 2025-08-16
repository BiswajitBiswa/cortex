import inspect
from typing import get_type_hints

import typer
import asyncio
import json
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# from yamcp.base_server import BaseServer
from yamcp.config import config
from yamcp.core.app import CoreApp
from yamcp.core.decorators import ToolBase
from yamcp.plugins.loader import register_plugins

typer_app = typer.Typer(no_args_is_help=True)
console = Console()


class CLIServer(CoreApp):
    def __init__(self, plugin_paths=None):
        super().__init__(plugin_paths)
        # self.core_app = CoreApp()
        # register_plugins(self.core_app, self.plugin_paths)
        self.setup_commands()

    @staticmethod
    def run():
        typer_app()

    def setup_commands(self):
        @typer_app.command()
        def discover(table_output: bool = typer.Option(False, "--table", help="Output as table (default: JSON)")):
            """List all available tools"""
            tools_info = []
            tools = self.list_tools()

            for name, tool_obj in tools.items():
                tool_data = {"tool_id": name}

                # Dynamically collect all public, non-callable attributes
                for attr in dir(tool_obj):
                    if attr.startswith("_"):
                        continue
                    val = getattr(tool_obj, attr)
                    if not callable(val):
                        tool_data[attr] = val

                # Extract `parameters` from function signature or `run()` method
                parameters = {}
                try:
                    if isinstance(tool_obj, ToolBase):
                        sig = inspect.signature(tool_obj.run)
                        hints = get_type_hints(tool_obj.run)
                    else:
                        sig = inspect.signature(tool_obj)
                        hints = get_type_hints(tool_obj)

                    for param in sig.parameters.values():
                        if param.name in ("self", "cls"):
                            continue
                        parameters[param.name] = hints.get(param.name, str).__name__
                except Exception as e:
                    parameters = {"error": f"Failed to parse: {str(e)}"}

                tool_data["parameters"] = parameters

                tools_info.append(tool_data)

            # 🖨️ Output
            if table_output:
                if not tools_info:
                    rprint("[red]No tools found.[/red]")
                    return

                # Gather all possible keys for table columns
                all_keys = sorted(set().union(*(tool.keys() for tool in tools_info)))

                table = Table(title="Available Tools")
                for key in all_keys:
                    table.add_column(key.upper(), style="bold green")

                for tool in tools_info:
                    row = []
                    for k in all_keys:
                        if k == "parameters":
                            val = tool.get(k, {})
                            param_str = ", ".join(f"{pk}: {pv}" for pk, pv in val.items())
                            row.append(param_str)
                        else:
                            row.append(str(tool.get(k, "")))
                    table.add_row(*row)

                console.print(table)
            else:
                console.print_json(data=tools_info)

        @typer_app.command()
        def run(tool: str, args: str = typer.Argument(None, help="JSON string of arguments")):
            """Run a tool with given args"""
            try:
                parsed_args = json.loads(args) if args else {}
            except json.JSONDecodeError:
                rprint("[red]Invalid JSON in args[/red]")
                raise typer.Exit(code=1)

            async def dispatch():
                result = await self.dispatch(tool, parsed_args)
                rprint(f"[green]Result:[/green] {result}")

            asyncio.run(dispatch())

        @typer_app.command()
        def info(tool: str):
            """Show metadata for a tool"""
            tools = self.list_tools()
            print(tools)
            tool_obj = tools.get(tool, None)
            if not tool_obj:
                rprint(f"[red]Tool '{tool}' not found.[/red]")
                raise typer.Exit(code=1)

            rprint("[bold cyan]Tool Metadata:[/bold cyan]")

            for attr in dir(tool_obj):
                if attr.startswith("_"):
                    continue  # Skip internal attributes
                val = getattr(tool_obj, attr)
                if not callable(val):
                    rprint(f"[yellow]{attr}[/yellow]: {val}")
