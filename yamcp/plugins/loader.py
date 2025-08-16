# logics/plugins/loader.py
import importlib.util
import os
import sys
import tempfile
import zipfile
import inspect
import urllib.request
from typing import get_type_hints

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

    def extract_parameters(obj):
        try:
            if isinstance(obj, ToolBase):
                sig = inspect.signature(obj.run)
                hints = get_type_hints(obj.run)
            else:
                sig = inspect.signature(obj)
                hints = get_type_hints(obj)

            params = {}
            for param in sig.parameters.values():
                if param.name in ("self", "cls"):
                    continue
                params[param.name] = hints.get(param.name, str).__name__
            return params
        except Exception as e:
            return {"error": f"Failed to parse: {str(e)}"}

    # Register decorated functions
    for name, obj in inspect.getmembers(module):
        if callable(obj) and is_tool(obj):
            core_app[getattr(obj, "name", name)] = obj

    # Register ToolBase subclasses
    for name, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, ToolBase) and cls is not ToolBase:
            instance = cls()
            # Dynamically add parameters attribute to instance
            cls.parameters = extract_parameters(instance)
            core_app[getattr(cls, "name", name)] = cls

    # Call explicit register() function if present
    if hasattr(module, "register"):
        module.register(core_app, app)
