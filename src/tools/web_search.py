from dotenv import load_dotenv
import os 
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=api_key)

def search(query)->list:
    """Search the web for the given query and return result titles and URLs."""
    result =[]
    response = client.search(
            query=query,
            max_results=5,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=False,
    )
    for i in response['results']:
        res = {
            "title": i["title"],
            "url": i["url"],
            "content": i.get("content", ""),
        }
        result.append(res)

    return result