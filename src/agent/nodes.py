
from src.agent.state import ResearchState
from  src.tools.web_search import search
from src.tools.scraper import scraper
from src.llm.llm import model

MAX_ITERATIONS = 2

def search_node(state: ResearchState):
    results = search(state.get("refined_query") or state["query"])
    return {
        "search_results": results
    }


def web_scraper_node(state : ResearchState):

    webpages = []
    seen = {s["url"] for s in state.get("summary", [])}

    for result in state["search_results"][:5]:

        if result["url"] in seen:
            continue

        try:
            page = scraper(result["url"])
            if page and page.get("content"):
                page["url"] = result["url"]
                webpages.append(page)

        except Exception:

            continue

    return {"webpages": webpages}


def summarizer_node(state: ResearchState):
    summaries = []
    for i in state['webpages']:

        title = i['title']
        content = i["content"][:15000]

        prompt = f"""
                    You are summarizing a webpage.

                    Title:
                    {title}

                    Content:
                    {content}

                    Provide:
                    - Main ideas
                    - Key facts
                    - Important numbers
                    - Conclusions
                """
        response = model.invoke(prompt)

        summaries.append({
            "title": title,
            "url": i["url"],
            "summary": response.content,
        })

    return {
        "summary" : summaries
    }


def reflect_node(state: ResearchState):

    prompt = f"""
        You are checking whether the collected summaries are enough to answer a research query.

        Query: {state["query"]}

        Summaries:
        {state["summary"]}

        If the summaries are enough to write a solid report, reply with exactly: SUFFICIENT
        Otherwise reply with only a better web search query, nothing else.
    """

    response = model.invoke(prompt)
    answer = response.content.strip()

    if "SUFFICIENT" in answer.upper():
        return {"refined_query": ""}

    return {
        "refined_query": answer,
        "iterations": state.get("iterations", 0) + 1,
    }


def should_continue(state: ResearchState):
    if state.get("refined_query") and state.get("iterations", 0) <= MAX_ITERATIONS:
        return "search_node"
    return "report_node"


def report_node (state: ResearchState):

    prompt = f"""
        Write a research report using only the provided summaries.

        Requirements:
        - Answer the query: {state["query"]}
        - Use citations with source URLs
        - Separate confirmed facts from uncertainty
        - Mention conflicting claims if sources disagree
        - Do not invent facts not present in the summaries

        Sources:
        {state["summary"]}
    """
    
    response = model.invoke(prompt)

    return {
        "report" : response.content
    }


