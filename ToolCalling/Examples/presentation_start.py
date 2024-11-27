from pprint import pprint

import ollama

client = ollama.Client(host='192.168.100.44')

from Lib.function_schematizer import ToolChain
import ToolCalling.Examples.tool_list as tool_list

tool_chain = ToolChain()
tool_chain.add_module(tool_list)

response = client.chat(
    model="llama3.2:latest",
    stream=False,
    messages=[
        {
            "role": "user",
            "content": "Is it sunny in Örebro?",
            "image": ["base64sdffghsdhgsfhjsdgsdfgdfghshrtdfsghfxcv"]
        },
        {'adsgdfhfgh'}
    ],
    tools=tool_chain.schemata
)

pprint(response)