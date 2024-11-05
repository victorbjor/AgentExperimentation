import json
from pprint import pprint
from typing import List

from langchain_core.tools import tool
from langchain_ollama import ChatOllama

import tool_list
from Lib.function_schematizer import ToolChain

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

llm = ChatOllama(
    base_url="192.168.255.67",
    model="llama3.1:70b",
    temperature=0,
).bind_tools(tool_chain.schemata)


message_history = [
    {
        'role': 'user',
        'content': 'Should I go to Skövde or Örebro today if I want some sun?'
    }
]

while True:
    message = llm.invoke(message_history)

    message_history.append(message)

    if message.content:
        print('Assistant says:', message.content)

    if not message.tool_calls:
        break

    for tool_call in message.tool_calls:
        name = tool_call['name']
        args = tool_call['args']
        result = tool_chain.call(name, args)
        print(f"Assistant calls: {name}({args}): {result}")
        message_history.append({
            'role': 'tool',
            'tool_call_id': tool_call['id'],
            'content': str(result),
        })

print('\n\n')
for message in message_history:
    if isinstance(message, dict):
        if message['role'] == 'tool':
            continue
        print('- ', message['content'])
    else:
        print('- ', message.content)