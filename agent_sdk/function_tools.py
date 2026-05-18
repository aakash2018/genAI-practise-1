from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool
)


# Disable tracing
set_tracing_disabled(True)

# -----------------------------------
# Ollama Cient
# -----------------------------------

client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# -----------------------------------
# Model
# -----------------------------------

model = OpenAIChatCompletionsModel(
    model="llama3.1",
    openai_client=client
)

# -----------------------------------
# Custom Web Search Tool
# -----------------------------------

@function_tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo
    """

    results = DDGS().text(query, max_results=5)

    output = []

    for r in results:
        output.append(
            f"Title: {r['title']}\n"
            f"Body: {r['body']}\n"
            f"Link: {r['href']}\n"
        )

    return "\n\n".join(output)

# -----------------------------------
# Agent
# -----------------------------------

agent = Agent(
    name="Assistant",
    instructions="""
    You are a helpful AI assistant.
    Use web_search tool when latest information is needed.
    """,
    model=model,
    tools=[web_search]
)

# -----------------------------------
# Memory
# -----------------------------------

messages = []

while True:

    input_query = input("\nYou: ")

    if input_query.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": input_query
    })

    # Run agent
    result = Runner.run_sync(
        agent,
        messages
    )

    reply = result.final_output

    print("\nAssistant:", reply)

    messages.append({
        "role": "assistant",
        "content": reply
    })