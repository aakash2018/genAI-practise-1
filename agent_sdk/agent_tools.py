# Hosted tools  => tools that are hosted by the agent provider and can be used by agents without any additional setup. Examples include search, calculator, and code execution tools.(websearchapi).
# function calling tools => tools that allow agents to call external APIs or functions. These tools require the agent developer to define the API or function and how to call it. Examples include a weather API tool or a stock price API tool.
# Agent as tools => tools that allow agents to call other agents as tools. This can be useful for creating more complex agents that can delegate tasks to other agents. For example, an agent that can answer questions about a specific topic could call another agent that is an expert in that topic to get the answer.

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , set_tracing_disabled
# from agents import WebSearchTool ollama not support web search tool yet, so commenting out for now

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
    model=model,
    tools=[]
    # tools=[WebSearchTool()]
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