from fastapi import FastAPI
from pydantic import BaseModel

from agent import agent

app = FastAPI(
    title="HobbyFi Copilot",
    version="1.0.0"
)

class ChatRequest(BaseModel):

    message: str

    thread_id: str = "vendor_1"

class ChatResponse(BaseModel):

    response: str

@app.post("/chat")

def chat(request: ChatRequest):

    config = {

        "configurable": {

            "thread_id": request.thread_id

        }

    }

    result = agent.invoke(

        {

            "messages": [

                {

                    "role": "user",

                    "content": request.message

                }

            ]

        },

        config=config

    )

    return ChatResponse(

        response=result["messages"][-1].content

    )
