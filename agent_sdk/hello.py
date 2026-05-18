from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , set_tracing_disabled

set_tracing_disabled(True)

# Ollama OpenAI-compatible client
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # dummy value
)

# Ollama model
model = OpenAIChatCompletionsModel(
    model="llama3",
    openai_client=client
)

# Agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful AI assistant",
    model=model
)

messages= [
    # {
    #     "role": "assistant",
    #     "content": "Welcome to the Ollama agent demo!"
    # },
]
input_query = input("Enter your query: ")

messages.append({
    "role": "user",
    "content": input_query
})
# Run
result = Runner.run_sync(
    agent,
    messages
)

print(result.final_output)