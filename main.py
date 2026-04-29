from ollama import chat
from ollama import ChatResponse

response:ChatResponse = chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Hi',
  },
]);

print(response)
print(response['message']['content'])
print(response['message']['content'])