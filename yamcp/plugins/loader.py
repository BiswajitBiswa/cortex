# logics/plugins/loader.py
import importlib.util
import os
import sys
import tempfile
import zipfile
import inspect
import urllib.request
from yamcp.core.decorators import is_tool, ToolBase


def register_plugins(core_app, plugin_paths, app=None):
    for path in plugin_paths:
        if path.startswith("http://") or path.startswith("https://"):
            with tempfile.TemporaryDirectory() as tmpdir:
                local_path = os.path.join(tmpdir, os.path.basename(path))
                urllib.request.urlretrieve(path, local_path)
                _register_plugin_from_path(core_app, local_path, app)
        else:
            _register_plugin_from_path(core_app, path, app)


def _register_plugin_from_path(core_app, path, app):
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".py"):
                full_path = os.path.join(path, file)
                _import_and_register(core_app, full_path, app)
    elif path.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(path, "r") as z:
                z.extractall(tmpdir)
            _register_plugin_from_path(core_app, tmpdir, app)
    elif path.endswith(".py"):
        _import_and_register(core_app, path, app)
    else:
        print(f"Unsupported plugin path: {path}")



def _import_and_register(core_app, filepath, app):
    modulename = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(modulename, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modulename] = module
    spec.loader.exec_module(module)

    # 1. Register decorated functions
    for name, obj in inspect.getmembers(module):
        if callable(obj) and is_tool(obj):
            core_app.register_tool(getattr(obj, "_tool_name", name), obj)

    # 2. Register ToolBase subclasses
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, ToolBase) and obj is not ToolBase:
            instance = obj()
            core_app.register_tool(instance.name, instance)

    # 3. If explicit register() function exists, call it
    if hasattr(module, "register"):
        module.register(core_app, app)
