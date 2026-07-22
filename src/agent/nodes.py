
from src.agent.state import ResearchState
from  src.tools.web_search import search
from src.tools.scraper import scraper
from src.llm.llm import model

def search_node(state: ResearchState):
    results = search(state['query'])
    return {
        "search_results": results
    }


def web_scraper_node(state : ResearchState):

    webpages = []

    for result in state["search_results"][:5]:

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


