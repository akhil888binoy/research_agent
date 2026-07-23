# Research Agent

A LangGraph research agent that takes a query, searches the web, scrapes the top results, summarizes each page with a local LLM, then judges whether the evidence is sufficient — looping back with a refined search query if not — before writing a cited research report.

The agency lives in `reflect_node`: the LLM decides at runtime how many search rounds to run and what to search for. The stages themselves run in a fixed order — a deliberate choice over a free-running tool-calling loop, since fixed stages are cheaper, more predictable, and easier to debug with a small local model.

## Graph

```
query → search_node → web_scraper_node → summarizer_node → reflect_node → report_node → report
                ↑                                              │
                └──────── refined query (max 2 loops) ─────────┘
```

- **search_node** — searches the web via [Tavily](https://tavily.com) (top 5 results), using the refined query on later iterations
- **web_scraper_node** — fetches each result and extracts title + paragraph text with BeautifulSoup, skipping URLs already summarized
- **summarizer_node** — summarizes each page (main ideas, key facts, numbers, conclusions); summaries accumulate across iterations
- **reflect_node** — the agentic step: the LLM decides if the summaries can answer the query; if not, it emits a refined search query and the graph loops back to search (capped at 2 extra rounds)
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
    graph.py             # LangGraph graph definition (with reflect loop)
    nodes.py             # search, scrape, summarize, reflect, report nodes
    state.py             # ResearchState TypedDict
  llm/
    llm.py               # ChatOllama model config
  tools/
    web_search.py        # Tavily search
    scraper.py           # requests + BeautifulSoup scraper
```
