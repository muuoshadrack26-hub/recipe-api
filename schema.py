from pydantic import BaseModel

class CreateUser(BaseModel):
    username:str
    password:str
    email:str

class UpdateUser(BaseModel):
    username:str
    password:str
    email:str

class CreateRecipe(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    cook_time: str
    category: str
class UpdateRecipe(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    cook_time: str
    category: str