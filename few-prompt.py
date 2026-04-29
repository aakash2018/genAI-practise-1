#few shot prompting example
from ollama import chat
from ollama import ChatResponse

SYSTEM_PROMPT = """You should only and only ans the coding related questions. Do not ans anything else. If user asks something other than coding, just say sorry.

Examples:
Q: can you explain the a+b whole square ?
A: sorry , I can only ans coding related questions.

Q: Hey Write a code in python for adding two numbers
A: def add(a,b):
    return a+b
"""
ChatResponse = chat(model='llama3', messages=[
    {
        'role': 'system',
        'content': SYSTEM_PROMPT
    },
    {
        'role': 'user',
        'content': 'Hey,can you explain a + b whole square ?',
    },
])
# print(ChatResponse)
# print(ChatResponse['message'])
print(ChatResponse['message']['content'])
# few shot prompting : the model is given a few examples before being asked to perform the task.
# Few-shot prompting ek technique hai jisme tum AI model ko kuch examples dene ke baad usse koi task dena start hota hai — aur model apni training ke base par answer deta hai.