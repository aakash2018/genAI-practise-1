#chain of thought outputs prompting example
import json
import re

from ollama import chat
from ollama import ChatResponse

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START,PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input),
    PLAN (That can be multiple times ) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    {"step":"START" or "PLAN" or "OUTPUT","content":"string"}

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: {"step":"PLAN","content":"Seems like user is interestd in math problem"}
    PLAN:{"step":"PLAN","content":"looking at the problem , we should solve this using BOSMAS method"}
    PLAN:{"step":"PLAN","content":"Yes, The BODMAS is correct thing to be done here"}
    PLAN:{"step":"PLAN","content":"first we must multiply 3 * 5 which is 15"}
    PLAN:{"step":"PLAN","content":"Now the new equation is 2 + 15/10"}
    PLAN:{"step":"PLAN","content":"we must perform divide that is 15/10 = 1.5"}
    PLAN:{"step":"PLAN","content":"Now the new equation is 2 + 1.5"}
    PLAN:{"step":"PLAN","content":"Now finally lets perform the add 3.5"}
    PLAN:{"step":"PLAN","content":"Great, we have solved and finally left with 3.5 as ans"}
    OUTPUT:{"step":"OUTPUT","content":"3.5"}

    Format:
    {"type":"json_object","content":{"step":"START" or "PLAN" or "OUTPUT","content":"string"}}
"""

print("\n\n\n")


message_history = [{
        'role': 'system',
        'content': SYSTEM_PROMPT
    }]

user_query =  input("User: ")

message_history.append({
    'role': 'user',
    'content': user_query
    })   

output_found = False

while True:
    response:ChatResponse = chat(model='llama3', messages=message_history)
    assistant_message = response['message']['content']
    json_blocks = re.findall(r'\{.*?\}', assistant_message, re.DOTALL)
    message_history.append({"role": "assistant", "content": assistant_message})
    print("Assistant:", assistant_message)

    if not json_blocks:
        print("❌ No JSON found")
        break

    for block in json_blocks:
        try:
            parsed_result = json.loads(block)
        except:continue

        if parsed_result.get("step") == "START":
            print("🔥", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "PLAN":
            print("🧠", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            output_found = True
            break

    if output_found:
        break

print("\n\n\n")

# response:ChatResponse = chat(model='llama3', messages=[
#     {
#         'role': 'system',
#         'content': SYSTEM_PROMPT
#     },
#     {
#         'role': 'user',
#         'content': 'Hey, write a code to add n numbers in js',
#     },
#     {
#         'role': 'assistant',
#         'content': json.dumps({"step": "START", "content": "You want a javascript code to add 'n' numbers."})
        
#     },
#     {
#         'role': 'assistant',
#         'content': json.dumps({"step": "PLAN", "content": "I need to provide a javascript function that can add any number of arguments or elements in an array. I will use the rest paramater syntax (...) to accept multiple numbers and then use the 'reduce' method to sum them up."})
#     },
#     {
#         'role': 'assistant',
#         'content': json.dumps({"step": "PLAN", "content": "I will define a Javascript function that accepts an arbitary number of arguments using the rest parameter. Inside the function, I will use the 'reduce' method to iterate through the numbers and calculate their sum. Finally, I will return the sum."})
#     },
#     {
#     'role': 'user',
#     'content': 'Now give OUTPUT'
#     }
# ])
# print(response)
# print(response['message'])
# print(response['message']['content'])
