from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from dotenv import load_dotenv
import os

from agent.tools import search_docs, search_docs_by_platform, get_code_example

load_dotenv()


def build_agent() -> AgentExecutor:
    """
    Builds and returns the agent executor.
    Call this once at startup and reuse the same instance.
    """

    # --- The LLM ---
    # This is the brain. gpt-4o-mini is cheap and more than
    # capable enough for tool-calling tasks like this.
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,        # 0 = consistent, factual answers (not creative)
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # --- The system prompt ---
    # This tells the agent who it is and how to behave.
    # The {agent_scratchpad} placeholder is where LangChain
    # injects the tool call results during the reasoning loop.
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
            You are a helpful assistant specialising in Android and iOS
            telemetry APIs. You help developers understand how to implement,
            query, and debug telemetry on mobile platforms.

            Always use your tools to search documentation before answering.
            Never answer from memory alone — always ground your response
            in the retrieved documentation.

            When you answer:
            - Be concise and practical
            - Mention which platform (Android/iOS) you are referring to
            - If you include code, keep it short and focused
            - Cite the source topic at the end of your answer
        """),
        MessagesPlaceholder(variable_name="chat_history"),  # For conversation memory
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # LangChain internals
    ])

    # --- Wire tools to the agent ---
    tools = [search_docs, search_docs_by_platform, get_code_example]

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    # AgentExecutor is the loop runner — it keeps calling tools
    # until the LLM decides it has enough info to answer.
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,   # Prints the reasoning steps — great for learning
        max_iterations=4,  # Safety limit — prevents infinite loops
    )

    return executor
