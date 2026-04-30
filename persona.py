#persona prompting example
from ollama import chat
from ollama import ChatResponse

SYSTEM_PROMPT = """You are an AI Persona Assistant named Amitabh Bachchan.
    You are acting on behalf of Amitabh Bachchan who is 70 years old Indian actor and 
    Singer.

    Examples:
    Q. Hey
    A: Hey, Whats up!
"""
response:ChatResponse = chat(model='llama3', messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role":"user", "content": "who are you?" }
])
# print(response)
# print(response['message'])
print(response['message']['content'])

# persona prompting ek technique hai jisme tum AI model ko ek specific character ya identity adopt karne ke liye instruct karte ho. Isme tum model ko ek detailed description dete ho us persona ke baare mein, jaise ki unka naam, unki background, unki personality traits, aur unke interests kya hain. Isse model us persona ke perspective se respond karta hai, jo ki user ke saath ek engaging aur personalized interaction create karta hai.
