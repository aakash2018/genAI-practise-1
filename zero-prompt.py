#zero shot prompting example
from ollama import chat
from ollama import ChatResponse

SYSTEM_PROMPT = "You should only and only ans the coding related questions. Do not ans anything else. If user asks something other than coding, just say sorry."
ChatResponse = chat(model='llama3', messages=[
    {
        'role': 'system',
        'content': SYSTEM_PROMPT
    },
    {
        'role': 'user',
        'content': 'Hey,can you wrie python program to print 2+2?',
    },
])
# print(ChatResponse)
# print(ChatResponse['message'])
print(ChatResponse['message']['content'])
# zero shot prompting : the model is given a direct question or task without prior examples.
# Zero-shot prompting ek technique hai jisme tum AI model ko koi example diye bina seedha instruction dete ho — aur model apni training ke base par answer deta hai.