import ollama
from pprint import pprint

import tool_list
from Lib.function_schematizer import ToolChain

MODEL_NAME = 'llama3.2:latest'

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

message_history = [
    {
        'role': 'user',
        'content': 'How are you feeling?'
    }
]

client = ollama.Client(host='192.168.100.44')

while True:
    response = client.chat(
        model=MODEL_NAME,
        messages=message_history,
        tools=tool_chain.schemata,
    )

    message_history.append(response['message'])

    if 'tool_calls' not in response['message'].keys():
        break

    for tool_call in response['message']['tool_calls']:
        name = tool_call['function']['name']
        args = tool_call['function']['arguments']
        print(f"Assistant calls: {name}({args})")
        result = tool_chain.call(name, args)
        message_history.append({
            'role': 'tool',
            'content': str(result),
        })

for message in message_history:
    print(message['content'])

