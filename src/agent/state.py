from typing import TypedDict

class ResearchState(TypedDict):
    query : str 
    search_results : list
    webpages : list 
    summary : list
    report : str
