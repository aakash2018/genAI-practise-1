#chain of thought outputs prompting example
import json
import os
import re
from pydantic import BaseModel, Field
from typing import Optional
import requests
from ollama import chat
from ollama import ChatResponse



def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START,PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    you can also call a tool if required from the list of available tools.
   for every tool call wait for the observe step which is the output from the called tool
     Rules:
    - Strictly Follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input),
    PLAN (That can be multiple times ) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    {"step":"START" | "PLAN" |"OUTPUT" | "TOOL","content":"string","tool":"string","input":"string"}

    Available Tools:
    - get_weather(city:str): This tool takes a city name as input and returns the current weather information for that city.

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


    Example 2:
    START: What is the weather of Delhi ?
    PLAN: {"step":"PLAN","content":"Seems like user is interestd in math problem"}
    PLAN:{"step":"PLAN","content":"let see if we have any available tool from the list of available tools"}
    PLAN:{"step":"PLAN","content":"Great, we have get_weather tool available for this query."}
    PLAN:{"step":"PLAN","content":"I need to call get_weather for Delhi as input for city"}
    PLAN:{"step":"TOOL","tool":"get_weather","input":"Delhi"}
    PLAN:{"step":"OBSERVE","tool":"get_weather","output":"the temp of delhi is cloudy with 20 degree celsius"}
    PLAN:{"step":"PLAN","content":"Great, I got the weather information for Delhi using the tool call and now I can provide the final OUTPUT to the user"}
    PLAN:{"step":"OUTPUT","content":"The weather in Delhi is cloudy with a temperature of 20 degree celsius."}
  
"""
print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")



message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]


while True:
    user_query = input("👉🏻 ")
    message_history.append({ "role": "user", "content": user_query })
    response:ChatResponse = chat(model='llama3', messages=message_history)
    raw_result = response['message']['content']
    message_history.append({"role": "assistant", "content": raw_result})

    json_blocks = re.findall(r'\{.*?\}', raw_result, re.DOTALL)

    if not json_blocks:
        print("❌ No JSON found")
        break

    print("🔍 JSON Blocks Found:", json_blocks[0])

    parsed_result = [json.loads(block) for block in json_blocks]

    print("✅ Parsed JSON:", parsed_result)

    for step_obj in parsed_result:
        if step_obj.get("step") == "START":
            print("🔥", step_obj.get("content"))
            continue

        if step_obj.get("step") == "TOOL":
            tool_to_call = step_obj.get("tool")
            tool_input = step_obj.get("input")
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")
            message_history.append({ "role": "developer", "content": json.dumps(
                { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
            ) })
            continue

        if step_obj.get("step") == "PLAN":
            print("🧠", step_obj.get("content"))
            continue

        if step_obj.get("step") == "OUTPUT":
            print("🤖", step_obj.get("content"))
            break

print("\n\n\n")
    