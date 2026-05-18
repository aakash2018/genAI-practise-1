from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import asyncio

from openai import AsyncOpenAI
set_tracing_disabled(True)
# Ollama OpenAI-compatible client
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # dummy value
)

# Ollama model
model = OpenAIChatCompletionsModel(
    model="qwen3",
    openai_client=client
)


spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=model
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=model
)


orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
    model=model
    
)

async def main():
    result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
    print(result.final_output)

asyncio.run(main())