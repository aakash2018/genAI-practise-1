from ollama import chat
from ollama import ChatResponse
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state:State):
    response:ChatResponse = chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': state.get("user_query"),
        },
    ]);

    state["llm_output"] = response['message']['content']
    return state

def evalaute_response(state:State) -> Literal["chatbot_gemini","endnode"]:

    ### 1. Basic NLP / ML Evaluation Metrics
    ### 2. LLM Evaluation Techniques
    ### 3. Human Evaluation
    ### 4. LLM-as-a-Judge
    ### 5. Chain-of-Thought (CoT) Evaluation
    ### 6. RAG Evaluation
    ### 7. Hallucination Detection
    ### 8. Agent evaluation
    ### 9. Benchmark creation
    ### 10. Self-Consistency Evaluation
    ### 11. Pairwise Comparison
    ### 12. Latency & Cost Evaluation
    ### 13. Safety Evaluation
    ### 14. Code Generation Evaluation
    if False:
        return "endnode"
    
    return "chatbot_gemini" 

def chatbot_gemini(state:State):
    response:ChatResponse = chat(model='gemma3:4b', messages=[
        {
            'role': 'user',
            'content': state.get("user_query"),
        },
    ]);

    state["llm_output"] = response['message']['content']
    return state

def endnode(state: State):
    print("endnode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evalaute_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 2 + 2?"}))
print(updated_state)