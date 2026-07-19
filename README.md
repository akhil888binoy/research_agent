# Research Agent

A small LangGraph-based research assistant that can search the web with Tavily,
scrape pages with `requests` and BeautifulSoup, and use a local Ollama chat
model to produce research answers.

## What It Does

- Runs a LangGraph agent loop with tool calling.
- Uses `gemma3:latest` through Ollama via `langchain-ollama`.
- Searches the web with Tavily.
- Scrapes article/page text from URLs returned by search.
- Uses a research-focused system prompt that encourages source checking and
  avoids unsupported claims.

## Project Structure

```text
.
├── main.py                  # Example async entry point
├── pyproject.toml           # Project metadata and dependencies
└── src
    ├── agents
    │   └── search.py        # Research assistant system prompt
    ├── llm
    │   └── llm.py           # Ollama model and tool binding
    ├── models
    │   └── state.py         # LangGraph state type
    ├── tools
    │   ├── scraper.py       # URL scraper tool
    │   └── web_search.py    # Tavily search tool
    └── workflow
        └── graph.py         # LangGraph workflow definition
```

## Requirements

- Python `>=3.14`
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Ollama](https://ollama.com/) running locally
- The `gemma3:latest` Ollama model installed
- A Tavily API key

Install the Ollama model:

```bash
ollama pull gemma3:latest
```

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

Make sure Ollama is running before invoking the agent:

```bash
ollama serve
```

## Usage

`main.py` currently defines an async `main()` function that creates the agent and
invokes it with an example question:

```python
result = await agent.ainvoke({
    "messages": [HumanMessage(content="How much did I spend on groceries?")]
})
```

To run it as a script, add the following to the bottom of `main.py`:

```python
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

Then run:

```bash
uv run python main.py
```

You can change the prompt in `main.py` to ask a different research question.

## How It Works

1. `main.py` calls `create_agent(tools)`.
2. `src/workflow/graph.py` builds a LangGraph `StateGraph`.
3. The `agent` node sends conversation messages to the Ollama model.
4. If the model requests a tool call, execution moves to the `tools` node.
5. The tool result is added to the message history.
6. The graph loops back to the agent until no more tool calls are needed.
7. The final assistant message is printed.

## Tools

### `search`

Defined in `src/tools/web_search.py`.

Uses Tavily to search the web and returns a list of result titles and URLs.

### `scraper`

Defined in `src/tools/scraper.py`.

Fetches a URL, parses the page HTML, and returns the page title plus paragraph
text.

## Configuration

The model is configured in `src/llm/llm.py`:

```python
model = ChatOllama(
    model="gemma3:latest",
    temperature=0
)
```

To use a different local model, update the `model` value and make sure the model
is installed in Ollama.

## Notes

- `TAVILY_API_KEY` is loaded from `.env` with `python-dotenv`.
- The current scraper handles HTTP errors by printing the error, but it does not
  return a structured error response for every failure path.
