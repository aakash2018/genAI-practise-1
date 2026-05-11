from ollama import chat
from ollama import ChatResponse


response:ChatResponse = chat(model='moondream', messages=[
  {
    'role': 'user',
    'content': "generate a caption for this image in about 50 words",
    'images':['./genAI-images-understand.jpg']
  },
]);

print(response.message['content'])