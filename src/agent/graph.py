
from src.agent.state import ResearchState
from langgraph.graph import StateGraph, START, END
from src.agent.nodes import report_node , summarizer_node , web_scraper_node , search_node

agent_builder = StateGraph(ResearchState)

agent_builder.add_node("search_node", search_node)
agent_builder.add_node("web_scraper_node", web_scraper_node)
agent_builder.add_node("summarizer_node", summarizer_node)
agent_builder.add_node("report_node", report_node)


agent_builder.add_edge(START , "search_node")
agent_builder.add_edge("search_node" , "web_scraper_node")
agent_builder.add_edge("web_scraper_node" , "summarizer_node")
agent_builder.add_edge("summarizer_node" , "report_node")
agent_builder.add_edge("report_node" , END)


