import os

from fastapi import FastAPI, APIRouter
import uvicorn

from yamcp.config import config
from yamcp.core.app import CoreApp
from yamcp.plugins.loader import register_plugins
from yamcp.transport.http import HTTPServer
from yamcp.transport.ws import WebSocketServer

app = FastAPI(title="APIS")

router = APIRouter()
import sys


# These are now initialized statically, only if RELOAD is on
# mode = os.getenv("YAMCP_MODE", "http_ws")
# plugin_paths = os.getenv("YAMCP_PLUGIN_PATHS", "plugins/").split(",")
# core_app = CoreApp()
# register_plugins(core_app, plugin_paths)


class HTTPWSServer:
    def __init__(self):
        self.core_app = CoreApp()
        self.plugin_paths = config.YAMCP_PLUGIN_PATHS
        register_plugins(self.core_app, self.plugin_paths)
        # self.plugin_paths = plugin_paths

        self.host = config.YAMCP_HOST
        self.port = config.YAMCP_PORT
        # self.mode = mode

        self.mode = config.YAMCP_MODE

        # Pass core_app to HTTP and WS servers (do NOT re-register plugins)
        if self.mode in ["http_ws", "http"]:
            print("included1")
            self.http_server = HTTPServer(core_app=self.core_app)
            router.include_router(self.http_server.router, prefix="/http", tags=["http"])
        if self.mode in ["http_ws", "ws"]:
            print("included2")
            self.ws_server = WebSocketServer(core_app=self.core_app)
            router.include_router(self.ws_server.router, prefix="/ws", tags=["ws"])

        app.include_router(router, prefix="/api")

    def run(self):
        # uvicorn.run(app, host=self.host, port=self.port)

        uvicorn.run("yamcp.http_ws_server:app", host=self.host, port=self.port, reload=True)


httpWSServer = HTTPWSServer()
