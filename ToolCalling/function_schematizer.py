import inspect
import json
from pprint import pprint
from typing import List, Dict


class ToolChain:
    def __init__(self):
        self.schemata = []
        self._call_map = {}

    def add_module(self, module):
        functions = inspect.getmembers(module, inspect.isfunction)
        for name, function in functions:
            print("Adding function:", name)
            self.schemata.append(function_to_schema(function))
            self._call_map[name] = function

    def call(self, function: str, arguments: str):
        return self._call_map[function](**arguments)


def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def schematize_module(module: object) -> List[Dict]:
    # Get all functions from the module
    functions = inspect.getmembers(module, inspect.isfunction)

    # List to store results
    results = []

    # Loop through all functions and call them
    for name, func in functions:
        results.append(function_to_schema(func))

    return results


# schema = function_to_schema(test_func)
# pprint(schema)
