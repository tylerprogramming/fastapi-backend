from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from my_agents.chatbot import ChatAgent

app = FastAPI(title="Simple FastAPI App")

# Add this before your endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: str | None = None

class UserInfo(BaseModel):
    id: str
    email: str

class ChatRequest(BaseModel):
    message: str
    user: UserInfo

assistant_agent = ChatAgent(name="Assistant", instructions="You are a helpful assistant")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_description": item.description}

@app.post("/chatbot/")
async def chatbot_endpoint(request: ChatRequest):
    response = await assistant_agent.get_response(request.message, request.user.id)
    return {"response": response} 