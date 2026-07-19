from dotenv import load_dotenv
import os 
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=api_key)

@tool
def search(query)->list:
    result =[]
    response = client.search(query)
    for i in response['results']:
        res= {
            'title' : i['title'],
            'url' : i['url']
        }
        result.append(res)

    return result

