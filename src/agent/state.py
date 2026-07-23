from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    query : str
    refined_query : str
    search_results : list
    webpages : list
    summary : Annotated[list, operator.add]
    report : str
    iterations : int
