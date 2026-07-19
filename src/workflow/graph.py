from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from src.llm.llm import llm_with_tools
from src.models.state import ResearchState
from src.agents.search import system_prompt

def create_agent(tools):

    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Define nodes
    async def call_agent(state: ResearchState):
        formatted = prompt.format_messages(messages=state["messages"])
        response = await llm_with_tools.ainvoke(formatted)
        return {"messages": [response]}
    
    def should_continue(state: ResearchState):
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END
    

    # Build graph
    workflow = StateGraph(ResearchState)
    workflow.add_node("agent", call_agent)
    workflow.add_node("tools", ToolNode(tools))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()