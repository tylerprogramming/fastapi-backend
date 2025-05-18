import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Todo(BaseModel):
    title: str
    user_id: str

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
    print("Creating todo")
    print(todo.model_dump())
    response = (
        supabase
        .table("todos")
        .insert(todo.model_dump())
        .execute()
    )
    print(response.data)
    return response.data

if __name__ == "__main__":
    print(get_all_todos())