from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from my_agents.chatbot import ChatAgent
from database import my_supabase as supabase_service
from models.models import Item, UserInfo, ChatRequest, Todo, RecommendedTodoInfo, TodoRecommendation
# from database.my_supabase import thumbs_up, thumbs_down

app = FastAPI(title="Simple FastAPI App")

# Add this before your endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant_agent = ChatAgent()

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

@app.post("/recommendations/")
async def recommendations_endpoint(request: UserInfo):
    response = supabase_service.get_three_recommendations(request.id)
    return {"response": response}

@app.post("/thumbs")
async def thumbs_up_endpoint(request: TodoRecommendation):
    if request.action == "up":
        print("the request is", request)
        response = supabase_service.thumbs_up(request)
    elif request.action == "down":
        response = supabase_service.thumbs_down(request)
    
    return {"response": response}