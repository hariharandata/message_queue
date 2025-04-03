from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str

class TaskResponse(TaskCreate):
    id: int
    status: str