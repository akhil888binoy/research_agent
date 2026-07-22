from src.agent.graph import agent_builder


def main():
    agent = agent_builder.compile()

    query = input("Research query: ")
    result = agent.invoke({"query": query})
    print(result["report"])


if __name__ == "__main__":
    main()
