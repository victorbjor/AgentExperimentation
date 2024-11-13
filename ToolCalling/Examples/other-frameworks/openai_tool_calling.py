import json
from openai import OpenAI

import tool_list
from Lib.function_schematizer import ToolChain

# Open AI
client = OpenAI()
MODEL_NAME='gpt-4o-mini'

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

# message_history = [
#     {
#         'role': 'user',
#         'content': 'Should I go to Skövde or Örebro today if I want some sun?'
#     }
# ]
message_history = [
    {
        'role': 'user',
        'content': 'Which city in Sweden has the best air quality today? Plan out your tool calling in advance, and state which tools you need to call, and in which order.'
    }
]

while True:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=message_history,
        tools=tool_chain.schemata,
    )

    message = response.choices[0].message
    message_history.append(message)

    if message.content:
        print('Assistant says:', message.content)

    if not message.tool_calls:
        break

    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = tool_chain.call(name, args)
        print(f"Assistant calls: {name}({args}): {result}")
        message_history.append({
            'role': 'tool',
            'tool_call_id': tool_call.id,
            'content': str(result),
        })


print(message_history)
# for message in message_history:
#     print(message['content'])

