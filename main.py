from fastapi import FastAPI, HTTPException 
from models.model import CreateUser, UserBase, Task, EditTask
from config.database import db

app = FastAPI()
user_collection = db.users
task_collection = db.tasks
def get_user(collection, user_id):
  print(db.users)
  return collection.find_one({'user_id': user_id})
  

@app.post('/admin/newuser/{admin_id}')
def adduser(admin_id, data:CreateUser):
    given_user = get_user(user_collection, admin_id)
    if given_user is None:
      raise HTTPException(status_code=404, detail='User is not found')
    else:
      if given_user['role'] == 'admin':
        user_collection.insert_one(dict(data))
      else:
        raise HTTPException(status_code=401, detail='User is not admin')
    

@app.put('/admin/updateuser/{admin_id}/{user_id}')
def update_user(admin_id, user_id, data:UserBase):
  user_collection = db.users
  given_user = get_user(user_collection, admin_id)
  if given_user is None:
    raise HTTPException(status_code=404, detail='User is not found')
  if given_user['role'] == 'admin':
    if data.name and data.role:
      user_collection.update_one({'user_id': user_id}, {'$set': {'name': data.name, 'role': data.role}})
    elif data.name == None:
      user_collection.update_one({'user_id': user_id}, {'$set': {'role': data.role}})
    elif data.role == None:
      user_collection.update_one({'user_id': user_id}, {'$set': {'name': data.name}})
    else:
      raise HTTPException(status_code=400, detail='Fields are Empty')
  else:
    raise HTTPException(status_code=401, detail='User is not admin')

@app.delete('/admin/{admin_id}/{user_id}')
def delete_user(admin_id, user_id):
  admin = get_user(user_collection, admin_id)
  if admin['role'] == 'admin':
    user_collection.delete_one({'user_id': user_id})
  else:
    raise HTTPException(status_code=401,detail='Admin_id is wrong')

@app.post('/create/{manager_id}/{user_id}')
def create_task(user_id, data:Task):
  manager = get_user(user_collection, manager_id)
  if (manager['role'] == 'admin') or (manager['role'] == 'manager'):
    assignedto_user = get_user(user_collection,user_id)
    if assignedto_user:
      task_collection.insert_one({'task_id': data.task_id, 'task': data.task_name, 'deadline': data.deadline, 'assigned_to': assignedto_user['user_id']})
    else:
      raise HTTPException(status_code=401, detail='user_id does not exist')
  else:
    raise HTTPException(status_code=401, detail='User is not admin or manager')
  
@app.put('/edit_task/{user_id}/{task_id}')
def edit_task(user_id, task_id, data:EditTask):
  user = get_user(user_collection, user_id)
  task = task_collection.find_one({'task_id': task_id})
  if task:  
    if user['role'] == 'admin' or user['role'] == 'manager':
      if task:
        task_collection.update_one({'task_id': task_id}, {'$set': {'task': data.task_name, 'deadline': data.deadline, 'assigned_to': data.assigned_to}})
      else:
        raise HTTPException(status_code=401, detail='Task does not exist')
    else:
      if task['assigned_to'] == user['user_id']:
        task_collection.update_one({'task_id': task_id}, {'$set': {'task': data.task_name, 'deadline': data.deadline, 'assigned_to': data.assigned_to}})
      else:
        raise HTTPException(status_code=401, detail='Task not does not belong to the User')
  else:
    raise HTTPException(status_code=401, detail='Task not does not belong ')

@app.get('/task/{user_id}')
def show_tasks(user_id):
  task_collection
  tasks =[]
  if get_user(user_collection, user_id):
    tasks = task_collection.find({'assigned_to': user_id})
  else:
    raise HTTPException(status_code=401, detail='User is not admin or manager')