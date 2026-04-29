from ollama import chat
from ollama import ChatResponse

ChatResponse = chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Hi',
  },
])
# print(ChatResponse)
# print(ChatResponse['message'])
print(ChatResponse['message']['content'])