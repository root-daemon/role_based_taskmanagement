from pydantic import BaseModel;
from typing import Optional;

class CreateUser(BaseModel):
  user_id:str
  name:str
  email:str
  role:str
  #role : admin or manager or user 
class UserBase(BaseModel):
  name: Optional[str]=None
  role: Optional[str]=None

class Task(BaseModel):
  task_id:str
  task_name: str
  completed: bool
  
class EditTask(BaseModel):
  task_name: Optional[str]=None
  deadline: Optional[str]=None
  assigned_to: Optional[str]=None