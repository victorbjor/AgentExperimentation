# Tool Calling with Ollama

### Installation
1. Pull this repo, obviously.
2. Install Ollama. https://ollama.com/download
3. Install python. https://www.python.org/downloads/
3. Pull a model file, like `ollama pull llama3.1:70b`
   1. Model files that currently support tool usage can be found here https://ollama.com/search?c=tools
   2. Make sure to check whether the model fits snuggly on your GPU for good performance
4. Install requirements.txt with `pip install -r requirements.txt`

### Usage
1. Fill up the module `tool_list.py` with any function you'll want your agent to be able to use.<br>
Make sure to use type hints and docstrings for the agent to be able to understand them.<br>
I have just put some dummy functions there at the moment, feel free to put whatever you want.

2. Set the model name on row 9 in `ollama_tool_calling.py` to a model that you have actually pulled. 
3. Run `ollama_tool_calling.py`
