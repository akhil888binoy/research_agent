from langchain_ollama import ChatOllama

model = ChatOllama(
    model='gemma3:latest',
    temperature=0
)
