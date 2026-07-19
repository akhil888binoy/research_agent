
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage

class ResearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "Conversation history"]

