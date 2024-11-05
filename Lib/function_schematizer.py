import inspect
import json
from pprint import pprint
from typing import List, Dict

from ToolCalling import tool_list


class ToolChain:
    def __init__(self):
        self.schemata = []
        self._call_map = {}
        self._properties_map = {}

    def add_module(self, module):
        functions = [e for e in inspect.getmembers(module) if inspect.isfunction(e[1]) and not e[0].startswith('_')]
        variables = [e for e in inspect.getmembers(module) if not inspect.isfunction(e[1]) and not e[0].startswith('_')]
        for name, function in functions:
            print("Adding function:", name)
            self.schemata.append(function_to_schema(function))
            self._call_map[name] = function
        for name, value in variables:
            print("Adding variable:", name, value)
            self._call_map[name] = lambda: value
            self.schemata.append(property_getter_to_schema(name, value))


    def add_object_methods(self, obj):
        # Get all public methods and properties from the object
        methods = [attr for attr in dir(obj) if callable(getattr(obj, attr)) and not attr.startswith('_')]
        properties = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith('_')]
        for method_name in methods:
            method = getattr(obj, method_name)
            print("Adding method:", method_name)
            self.schemata.append(function_to_schema(method))
            self._call_map[method_name] = method
        for prop_name in properties:
            prop_value = getattr(obj, prop_name)
            print(f"Adding property: {prop_name} with value {prop_value}")
            self._call_map[prop_name] = lambda: getattr(obj, prop_name)
            self.schemata.append(property_getter_to_schema(prop_name, prop_value))




    def view_properties(self):
        # Pretty print the public properties
        from pprint import pprint
        pprint(self._properties_map)

    def call(self, function: str, arguments: dict = None):
        if arguments is None:
            arguments = {}
        if function in self._call_map:
            # Call the function or property getter
            return self._call_map[function](**arguments) if callable(self._call_map[function]) else self._call_map[function]()
        raise ValueError(f"Function or property '{function}' not found")

    def pprint(self):
        from pprint import pprint
        pprint(self.schemata)

    def clear(self):
        self.schemata = []
        self._call_map = {}
        self._properties_map = {}


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


def property_getter_to_schema(prop_name: str, prop_value) -> dict:
    """Creates a schema for the property getter function."""
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    prop_type = type(prop_value)
    schema_type = type_map.get(prop_type, "string")

    return {
        "type": "function",
        "function": {
            "name": prop_name,
            "description": f"Getter function for property '{prop_name}' of type {schema_type}",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
            "returns": {
                "type": schema_type,
            },
        },
    }


if __name__ == "__main__":
    # Example Usage
    class ExampleClass:
        def __init__(self, value):
            self.public_property = value
            self.another_property = 42
            self._private_property = "hidden"

        def public_method(self, name: str):
            """This is a public method"""
            return f"Hello, {name}!"

        def _private_method(self):
            """This is a private method"""
            pass


    example_obj = ExampleClass("example_value")

    tool_chain = ToolChain()
    tool_chain.add_object_methods(example_obj)  # Add public methods of the object

    tool_chain.pprint()  # Prints method and property descriptions

    # Call a method
    result = tool_chain.call("public_method", {"name": "Dan"})
    print(result)

    # Call a property
    property_value = tool_chain.call("public_property")
    print(property_value)

    #### NEW
    tool_chain = ToolChain()
    tool_chain.add_module(tool_list)
    # tool_chain.pprint()
    tool_chain.call('private_api_key')
