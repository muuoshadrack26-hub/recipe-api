from datetime import datetime
from symtable import Class

from sqlmodel import SQLModel, Field


class User(SQLModel,table=True):
    user_id:int | None=Field(default=None,primary_key=True)
    username:str
    email:str
    hashed_password:str

class Recipe(SQLModel,table=True):
    recipe_id:int |None=Field(default=None,primary_key=True)
    title:str
    description:str
    ingredients:str
    instructions:str
    cook_time:str
    category:str
    owner_id:int
    created_at:datetime



