# Research Workflow

A LangGraph agent that takes a research query, searches the web, scrapes the top results, summarizes each page with a local LLM, and writes a cited research report.

## Pipeline

```
query → search_node → web_scraper_node → summarizer_node → report_node → report
```

- **search_node** — searches the web via [Tavily](https://tavily.com) (top 5 results)
- **web_scraper_node** — fetches each result and extracts title + paragraph text with BeautifulSoup
- **summarizer_node** — summarizes each page (main ideas, key facts, numbers, conclusions)
- **report_node** — writes a final report with source citations, separating confirmed facts from uncertainty

The LLM is `gemma3` running locally via [Ollama](https://ollama.com).

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com) with the `gemma3` model pulled (`ollama pull gemma3`)
- A [Tavily](https://tavily.com) API key

## Setup

```bash
uv sync
```

Create a `.env` file in the project root:

```
TAVILY_API_KEY=your-key-here
```

## Usage

```bash
uv run main.py
```

Enter a research query at the prompt; the report prints to stdout.

## Project structure

```
main.py                  # CLI entry point
src/
  agent/
    graph.py             # LangGraph graph definition
    nodes.py             # search, scrape, summarize, report nodes
    state.py             # ResearchState TypedDict
  llm/
    llm.py               # ChatOllama model config
  tools/
    web_search.py        # Tavily search
    scraper.py           # requests + BeautifulSoup scraper
```
