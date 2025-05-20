import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from models.models import Todo, RecommendedTodoInfo, UserInfo, TodoRecommendation

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_all_todos(user_id: str):
    response = (
        supabase
        .table("todos")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )   
    return response.data

def create_todo(todo: Todo):
    response = (
        supabase
        .table("todos")
        .insert(todo.model_dump())
        .execute()
    )
    return response.data

def get_three_recommendations(user_id: str) -> List[Todo]:
    response = (
        supabase
        .table("recommended_todos")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data

def thumbs_up(request: TodoRecommendation):
    todo = {
        "id": request.todo.id,
        "title": request.todo.title,
        "user_id": request.user.id
    }
    
    response = (
        supabase
        .table("todos")
        .insert(todo)
        .execute()
    )
    
    deleted_todo = (
        supabase 
        .table("recommended_todos")
        .delete(returning="minimal")
        .eq("title", request.todo.title)
        .execute()
    )
    
    return response.data

def thumbs_down(request: TodoRecommendation):
    response = (
        supabase
        .table("recommended_todos")
        .delete(returning="minimal")
        .eq("title", request.todo.title)
        .execute()
    )
    
    return response.data

if __name__ == "__main__":
    print(get_all_todos())