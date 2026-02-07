import pytest
from src.core.state import AgentState
from langchain_core.messages import HumanMessage

def test_agent_state():
    state: AgentState = {
        "messages": [HumanMessage(content="Hello")],
        "next": "Researcher",
        "context": {}
    }
    assert len(state["messages"]) == 1
    assert state["next"] == "Researcher"
