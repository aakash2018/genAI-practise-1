from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from typing import Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver

llm = init_chat_model(model="llama3",model_provider="ollama")

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages":[response]}


# graph_builder = StateGraph[]()
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph = graph_builder.compile()

MONGODB_URI = "mongodb://admin:admin@localhost:27017"
DB_NAME = "checkpoint_example"

def compile_graph_with_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpoint(checkpointer=checkpointer)

    config = {
        "configurable":{
            "thread_id":"Aakash"
        }
    }

    for chunk in graph_with_checkpoint.stream(State({
            "messages": [
                HumanMessage(
                    content="Hi, my name is Aakash Prajapat"
                )
            ]
        }), config=config,stream_mode="values"):
        chunk["messages"][-1].pretty_print()

    # print("\n\nupdated_state:", updated_state)

#nodes is nothing a function that do specific task.