import os 
from mem0 import Memory
from ollama import chat
from ollama import ChatResponse
import json

config = {
    "version": "v1.1",
    "embedder": {
        "provider":"ollama",
        "config":{
            "model":"nomic-embed-text"
        }
    },
    "llm":{
        "provider":"ollama",
        "config":{
            "model":"llama3"
        }
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port":6333,
            "collection_name": "aakash_memory",
            "embedding_model_dims": 768
        }
    }
}


mem_client = Memory.from_config(config)
print(mem_client.vector_store.collection_name)


while True:

    user_query = input("\nWhat do you want to ask? --->")

    search_memory = mem_client.search(query=user_query, filters={"user_id": "aakash"})

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]

    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    response:ChatResponse=chat(model="llama3", messages=[{ "role": "system", "content": SYSTEM_PROMPT },{"role": "user", "content": user_query}])

    ai_response = response.message['content']

    print("AI:", ai_response)

    # search_memory = mem_client.search(query=user_query, user_id="aakash") 
    # mem_client.add(
    #     [{"role": "user", "content": user_query}, {"role": "assistant", "content": ai_response}],user_id="aakash")

    mem_client.add(
        [{"role": "user", "content": user_query}, {"role": "assistant", "content": ai_response}],user_id="aakash")


print("Memory added successfully!")
