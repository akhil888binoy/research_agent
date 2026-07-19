from langchain_core.messages import BaseMessage, HumanMessage
from src.workflow.graph import create_agent
from src.llm.llm import tools



async def main():
    agent = create_agent(tools)
        
    # Run agent
    result = await agent.ainvoke({
            "messages": [HumanMessage(content="How much did I spend on groceries?")]
    })
        
        # Get final response
    final_response = result["messages"][-1].content
    print(final_response)