import os

from agents import Agent, Runner
from dotenv import load_dotenv
from typing import Any, List
from pydantic import BaseModel
from agents import function_tool
from database.my_supabase import get_all_todos, create_todo, get_three_recommendations
from models.models import Todo
from my_agents.prompts import todo_prompt, recommendation_prompt

load_dotenv()

@function_tool
def get_todos(user_id: str):
    return get_all_todos(user_id)

@function_tool
def add_todo(todo: Todo):
    return create_todo(todo)

@function_tool
def get_recommendations(user_id: str) -> List[Todo]:
    return get_three_recommendations(user_id)

class ChatAgent:
    def __init__(self):
        self.chatbot_agent = Agent(
            name="Assistant", 
            instructions="You are a helpful assistant", 
            tools=[get_todos, add_todo]
        )
        self.recommendation_agent = Agent(
            name="Recommendation Agent",
            instructions="You are a recommendation agent that recommends todos to users based on the knowledge of the user's preferences.",
            tools=[get_recommendations],
            output_type=List[Todo]
        )
        
    async def get_response(self, message: str, user_id: str) -> str:
        complete_message = f"The prompt is: {todo_prompt} \n\n The user's message is: {message} \n\n User ID: {user_id}"
        result = await Runner.run(self.chatbot_agent, complete_message)
        return result.final_output
    
    async def get_recommendations(self, user_id: str) -> List[Todo]:
        complete_message = f"The prompt is: {recommendation_prompt} \n\n User ID: {user_id}"
        result = await Runner.run(self.recommendation_agent, complete_message)
        print("this is the result", result.final_output)
        return result.final_output