from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from typing import Annotated

class State(TypedDict):
    messages: Annotated[list,add_messages]


graph_builder = StateGraph[State]()