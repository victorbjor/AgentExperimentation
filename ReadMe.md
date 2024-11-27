# Tool Calling with Ollama

### Installation
1. Install python. https://www.python.org/downloads/
   <br>_(You may skip step 3 if you don't plan to serve LLM locally)_
2. Install Ollama. 
   1. https://ollama.com/download 
   2. After installing, pull a model file, like `ollama pull llama3.2`
   3. Model files that currently support tool usage can be found here https://ollama.com/search?c=tools
   4. Make sure to check whether the model fits snuggly on your GPU for good performance
3. Install PyTorch for your system. https://pytorch.org/get-started/locally/
4. Pull this repo.
   1. Run `pip install -e .` in the root directory of the repo.
   2. If you run into problems add the repo root dir to `PYTHONPATH`.

### Tool Calling
There are examples of how to use this in `/ToolCalling/Examples/`
1. In the Lib module there is a class called ToolChain. Import it and add modules or objects that hold methods and properties to an instance of it.

```python
import ToolCalling.Examples.tool_list as tool_list
from Lib.function_schematizer import ToolChain

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

# Make sure to use type hints and docstrings for the agent to be able to understand them
```

#### Examples of tools to try
- API calls
- Calculator
- Pass the user to someone else
- `import playwright` and go bananas


# Workshop

Look through the different directories and get inspired by the examples

Then choose your own project and implement it!


### Topic Suggestions:

- Refine answer by asking the user to clarify what they need.
- Solve math problems by giving the agent a calculator tool and maybe some step by step reasoning.
- Make a bot that translates text and then iteratively improves it.
- Give the bot access to your API of choice.
- `import playwright` and let the LLM control a web page
