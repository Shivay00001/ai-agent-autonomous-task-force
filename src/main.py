import asyncio
from src.graphs.task_force import create_task_force_graph
from langchain_core.messages import HumanMessage

async def main():
    graph = create_task_force_graph()
    
    initial_state = {
        "messages": [HumanMessage(content="Determine the current price of Bitcoin and write a short summary of its performance this week.")],
        "context": {}
    }
    
    async for event in graph.astream(initial_state):
        for node_name, output in event.items():
            print(f"--- Node: {node_name} ---")
            if "messages" in output:
                print(output["messages"][-1].content)
            elif "next" in output:
                print(f"Routing to: {output['next']}")

if __name__ == "__main__":
    asyncio.run(main())
