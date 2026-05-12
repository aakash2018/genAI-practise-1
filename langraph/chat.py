from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from typing import Annotated
from langchain_core.messages import HumanMessage, AIMessage

llm = init_chat_model(model="llama3",model_provider="ollama")

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages":[response]}

def sample_node(state: State):
    print("\n\n Inside the sample node",state)
    return {"messages":[AIMessage(content="Hi,This is a message from sample node")]}


# graph_builder = StateGraph[]()
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_node("sample_node",sample_node)   

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sample_node")
graph_builder.add_edge("sample_node",END)

graph = graph_builder.compile()

updated_state=graph.invoke({
        "messages": [
            HumanMessage(
                content="Hi, my name is Aakash Prajapat"
            )
        ]
    })

print(updated_state)

#nodes is nothing a function that do specific task.