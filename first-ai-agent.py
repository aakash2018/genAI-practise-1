from ollama import chat
from ollama import ChatResponse
import requests

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%c+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    
    return "Sorry, I couldn't fetch the weather information right now." 

print(get_weather("New York"))

def main():
    user_query =  input("User: ")
    response:ChatResponse = chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': user_query
    }
    ])
    print(response['message']['content'])

main()

