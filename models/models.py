from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

class UserInfo(BaseModel):
    id: str
    email: str

class ChatRequest(BaseModel):
    message: str
    user: UserInfo
    
class Todo(BaseModel):
    title: str
    user_id: str
    
class RecommendedTodoInfo(BaseModel):
    title: str
    id: str
    
class TodoRecommendation(BaseModel):
    todo: RecommendedTodoInfo
    action: str  # 'up' or 'down'
    user: UserInfo 