import os

from agents import Agent, Runner
from dotenv import load_dotenv
from typing import Any
from pydantic import BaseModel
from agents import function_tool
from database.my_supabase import get_all_todos, create_todo

load_dotenv()

todo_prompt = """
You are an AI assistant responsible for managing a user's todo list. Your goal is to understand the user's request and select the appropriate tool to interact with their todo list. Todo items in this system only consist of **text** and a **completion status** (either completed or pending). You MUST respond with a JSON object specifying the tool to be called and its parameters.
Using the available tools
- Get all todos for a user
- Create a new todo for a user (or multiple)
- Update the completion status of a todo
- Delete a todo
"""

class Todo(BaseModel):
    title: str
    user_id: str

@function_tool
def get_todos(user_id: str):
    return get_all_todos(user_id)

@function_tool
def add_todo(todo: Todo):
    return create_todo(todo)

class ChatAgent:
    def __init__(self, name: str, instructions: str):
        self.agent = Agent(
            name=name, 
            instructions=instructions, 
            tools=[get_todos, add_todo]
        )

    async def get_response(self, message: str, user_id: str) -> str:
        complete_message = f"The prompt is: {todo_prompt} \n\n The user's message is: {message} \n\n User ID: {user_id}"
        result = await Runner.run(self.agent, complete_message)
        return result.final_output