import requests
import speech_recognition as sr
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio
import pyttsx3

client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # kuch bhi string de sakte ho
)



async def tts(speech: str):
    response = await client.chat.completions.create(
        # model="legraphista/Orpheus:3b-ft-q2_k",
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": """
                Always speak in cheerful manner with full of delight and happy.
                Generate expressive TTS friendly text.
                """
            },
            {
                "role": "user",
                "content": speech
            }
        ]
    )

    print(response,"ttt====================>")
    print(response.model_dump_json(indent=2))
    voice_texts = response.choices[0].message.content

    local_engine = pyttsx3.init()

    local_engine.setProperty("rate", 170)
    local_engine.setProperty("volume", 1.0)

    print(voice_texts,"ttt")
    local_engine.say(voice_texts)
    local_engine.runAndWait()
    # yaha apna audio player / TTS engine use karo
    # await LocalAudioPlayer().speak(ai_text)

    # cleanup
    local_engine.stop()
    # async with client.audio.speech.with_streaming_response.create(
    #     model="gpt-4o-mini-tts",
    #     voice="coral",
    #     instructions="Always speak in cheerfull manner with full of delight and happy",
    #     input=speech,
    #     response_format="pcm",
    # )as response:
    #     await LocalAudioPlayer().play(response)
        

async def first():
    r = sr.Recognizer() #speech to text
    with sr.Microphone() as source: #mic access
       
        r.adjust_for_ambient_noise(source) #noise cancellation
        r.pause_threshold = 2 #pause threshold

        SYSTEM_PROMPT = f"""
                You're an expert voice agent. You are given the transcript of what
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user.
        """
        messages = [
            { "role": "system", "content": SYSTEM_PROMPT },
        ]

        while True:
          
          try:

            print("Speak Something...")
            audio = r.listen(source) #listen to the mic

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio) #speech to text using google api

            print("You said:", stt)

            print("Sending to LLM...")
            messages.append({
                        "role": "user",
                        "content": stt
                    })  
            payload = {
                # "model": "tinyllama:latest",
                "model":"qwen2.5:1.5b",
                "messages": messages,
                "stream": False
            }

            url = "http://localhost:11434/api/chat"
            
            response = requests.post(url, json=payload)
            #   print(response.json().get("message").get("content"),"works")
            data = response.json()
            print(data)
            ai_text = data["message"]["content"]
            #   ai_text = response.json().get("message").get("content")
            await tts(speech=ai_text)
          except Exception as e:
                print("Error:", e)


asyncio.run(first())

    