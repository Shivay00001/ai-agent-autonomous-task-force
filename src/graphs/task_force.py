from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from src.core.state import AgentState
from src.agents.base import create_agent, agent_node
from src.agents.supervisor import create_supervisor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage

def create_task_force_graph():
    llm = ChatOpenAI(model=settings.MODEL_NAME)
    
    # 1. Define Tools
    search_tool = TavilySearchResults(max_results=3)
    
    # 2. Define Agents
    researcher_agent = create_agent(
        llm, 
        [search_tool], 
        "You are a meticulous researcher. Search for accurate information and summarize findings."
    )
    
    writer_agent = create_agent(
        llm, 
        [], 
        "You are a professional writer. Use the research provided to create high-quality content."
    )
    
    supervisor = create_supervisor(llm, ["Researcher", "Writer"])
    
    # 3. Build Graph
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("Researcher", lambda state: agent_node(state, researcher_agent, "Researcher"))
    workflow.add_node("Writer", lambda state: agent_node(state, writer_agent, "Writer"))
    workflow.add_node("supervisor", supervisor)
    
    # Define Edges
    workflow.add_edge("Researcher", "supervisor")
    workflow.add_edge("Writer", "supervisor")
    
    # Conditional Edges from Supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "Researcher": "Researcher",
            "Writer": "Writer",
            "FINISH": END
        }
    )
    
    workflow.set_entry_point("supervisor")
    
    return workflow.compile()
