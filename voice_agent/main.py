import requests
import speech_recognition as sr


def main():
    r = sr.Recognizer() #speech to text
    with sr.Microphone() as source: #mic access
          SYSTEM_PROMPT = f"""
                You're an expert voice agent. You are given the transcript of what
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user.
            """
          r.adjust_for_ambient_noise(source) #noise cancellation
          r.pause_threshold = 2 #pause threshold

          print("Speak Something...")
          audio = r.listen(source) #listen to the mic

          print("Processing Audio... (STT)")
          stt = r.recognize_google(audio) #speech to text using google api

          print("You said:", stt)

          print("Sending to LLM...")

          payload = {
            "model": "tinyllama:latest",
            "messages": [
                { "role": "system", "content": SYSTEM_PROMPT },
                {
                    "role": "user",
                    "content": stt
                }
            ],
            "stream": False
          }

          url = "http://localhost:11434/api/chat"
          
          response = requests.post(url, json=payload)
          print(response.json().get("message").get("content"),"works")

main()

    