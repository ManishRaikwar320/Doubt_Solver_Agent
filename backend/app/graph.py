import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt, Command
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
#from app.Database.redis_checkpoint_memory import redis_checkpoint

# RAG
from app.rag.retriever import retrieve_context


#0. Config
import os

xkiro_api_key = os.getenv("XKIRO_API_KEY")
if not xkiro_api_key:
    raise ValueError("XKIRO_API_KEY environment variable set nahi hai!")



memory = InMemorySaver() #redis_checkpoint()

# 1. LLM
def get_llm():
    return ChatOpenAI(
    model="qwen/qwen3.8-max:free",
    base_url="https://api.xkiro.com/v1",
    api_key=xkiro_api_key,
    temperature=0.2,
    max_tokens=500
)

# 2. Define State
class BotState(TypedDict, total=False):
    
    question: str
    context: str
    sources: list[str]
    bot_response: str
    answer_mode: str


# 3. Nodes Define
def Retrieve_Node(state: BotState):
    result = retrieve_context(question=state["question"], k=4)
    return {
        "context": result["context"],
        "sources": result["sources"]
    }


def Ask_Agent(state: BotState):

    answer_mode = interrupt(
        {
            "message": "Choose Your Answer Length",
            "Options": ["Short", "Medium", "Long"]
        }
    )

    llm = get_llm()
    context = state.get("context") or "No relevant context found."

    system_prompt = f"""
        You are an expert AI Doubt Solver. Help students understand concepts clearly.

        Detail Level Instruction: {answer_mode}

        Study Material (retrieved from the student's uploaded pages):
        {context}

        General Guidelines:
        1. Answer mainly using the study material above.
        2. If the material doesn't cover the question, say so clearly,
           then answer from your own knowledge.
        3. Ensure high technical accuracy and break complex points step-by-step.
        4. Avoid unnecessary filler text.
    """

    response = llm.invoke(
        [
            SystemMessage(
                content=system_prompt
            ),
            HumanMessage(
                content=state["question"]
            )
        ]
    )

    return { "bot_response": response.content }



# 4. Graph Build
def agent_graph():

    graph = StateGraph(BotState)

    # Nodes
    graph.add_node("retrieve_node", Retrieve_Node)
    graph.add_node("bot_node", Ask_Agent)

    # Edges
    graph.add_edge(START, "retrieve_node")
    graph.add_edge("retrieve_node", "bot_node")
    graph.add_edge("bot_node", END)

    return graph.compile(checkpointer=memory)

graph = agent_graph()


def invoke_function(graph, message, thread_id):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = graph.get_state(config)
    pending = any(t.interrupts for t in state.tasks)

    if pending:
        inp = Command(resume=message)
    else:
        inp = {"question": message}

    result = graph.invoke(inp, config)

    if "__interrupt__" in result:
        return {
            "status": "waiting_for_human",
            "interrupt": result["__interrupt__"][0].value,
        }

    # Graph poora ho gaya
    return {
        "status": "done",
        "bot_response": result["bot_response"],
        "sources": list(dict.fromkeys(result.get("sources", []))),  # unique, order same
    }

if __name__ == "__main__":

    thread_id = "doubt-1"

    while True:
        message = input("Bot:- ")

        response  = invoke_function(graph=graph, message=message, thread_id=thread_id)
        print(response)