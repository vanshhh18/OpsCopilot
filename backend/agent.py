from langchain_groq import ChatGroq

from langgraph.prebuilt import create_react_agent

from tools import TOOLS

from prompt import SYSTEM_PROMPT

from memory import memory

from config import GROQ_API_KEY


# ----------------------------------------
# Initialize LLM
# ----------------------------------------

llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    api_key=GROQ_API_KEY,

    temperature=0

)


# ----------------------------------------
# Create Agent
# ----------------------------------------

agent = create_react_agent(

    model=llm,

    tools=TOOLS,

    prompt=SYSTEM_PROMPT,

    checkpointer=memory

)