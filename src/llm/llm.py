from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from src.tools.web_search import search
from src.tools.scraper import scraper

model = ChatOllama(
    model='gemma3:latest',
    temperature=0
)

tools =[search , scraper]
llm_with_tools = model.bind_tools(tools)
tool_node = ToolNode(tools)