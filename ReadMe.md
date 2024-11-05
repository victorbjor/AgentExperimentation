# Tool Calling with Ollama

### Installation
1. Pull this repo, obviously.
2. Install Ollama. https://ollama.com/download
3. Install python. https://www.python.org/downloads/
3. Pull a model file, like `ollama pull llama3.2`
   1. Model files that currently support tool usage can be found here https://ollama.com/search?c=tools
   2. Make sure to check whether the model fits snuggly on your GPU for good performance
4. Install PyTorch for your system. https://pytorch.org/get-started/locally/
5. Install requirements.txt with `pip install -r requirements.txt`

### Tool Calling
There are examples of how to use this in `/ToolCalling/Examples/`
1. In the Lib module there is a class called ToolChain. Import it and add modules or objects that hold methods and properties to an instance of it.

```python
import tool_list # Or wherever you keep the files you want to use
from Lib.function_schematizer import ToolChain

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

# Make sure to use type hints and docstrings for the agent to be able to understand them
```
