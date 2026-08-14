import secrets
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy import func
from database import lifespan,SessionDep
from schema import CreateUser,UpdateUser,CreateRecipe,UpdateRecipe
from model import User,Recipe
from auth import pwd_context,create_access_token,get_current_user


app=FastAPI(lifespan=lifespan)



@app.post("/user")
async def create_user(new_user:CreateUser,session:SessionDep):
    hashed=pwd_context.hash(new_user.password)
    user=User(
        username=new_user.username,
        hashed_password=hashed,
        email=new_user.email
    )
    existing=session.exec(select(User).where(User.username==new_user.username)).first()
    if existing:
        raise HTTPException(status_code=403,detail="user exists")
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
@app.get("/user")
async def get_user(session:SessionDep,current_user:User=Depends(get_current_user)):
    user=session.exec(select(User).where(User.user_id==current_user.user_id)).first()
    return user
@app.put("/user")
async def update_user(updated_user:UpdateUser,session:SessionDep,current_user:User=Depends(get_current_user)):
    user=session.get(User,current_user.user_id)

    user.username=updated_user.username
    user.hashed_password=pwd_context.hash(updated_user.password)
    user.email=updated_user.email
    session.commit()
    session.refresh(user)

    return {"updated_user":user}

@app.delete("/user")
async def delete_user(session:SessionDep,current_user:User=Depends(get_current_user)):
    user=session.get(User,current_user.user_id)
    if user is None:
        raise HTTPException(404,"user not found")
    session.delete(user)
    session.commit()

    return {"deleted":"successfully"}


#-----------------------------------login----
@app.post("/login")
async def login(session:SessionDep,form_data:OAuth2PasswordRequestForm=Depends()):
    user=session.exec(select(User).where(User.username==form_data.username)).first()
    if user is None:
        raise HTTPException(404,"not found")
    verif=pwd_context.verify(form_data.password,user.hashed_password)
    if not verif:
        raise HTTPException(401,"unauthorized")
    access_token=create_access_token(data={"sub":user.username})

    return {"access_token":access_token,
            "token_type":"bearer"}
#----------------------------------recipes------
@app.post("/recipe")
async def create_recipes(new_recipe:CreateRecipe,session:SessionDep,current_user:User=Depends(get_current_user)):

    recipe=Recipe(
        title=new_recipe.title,
        description=new_recipe.description,
        ingredients=new_recipe.ingredients,
        instructions=new_recipe.instructions,
        cook_time=new_recipe.cook_time,
        category=new_recipe.category,
        owner_id=current_user.user_id,
        created_at=datetime.now()


    )
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return {"new_recipe":recipe}

@app.get("/recipe/{recipe_id}")
async def get_recipe(recipe__id:int,session:SessionDep,current_user:User=Depends(get_current_user)):
    recipe=session.get(Recipe,recipe__id)
    print("Recipe owner:", recipe.owner_id)
    print("Current user:", current_user.user_id)
    if recipe.owner_id != current_user.user_id:
        raise HTTPException(status_code=401,detail="unauthorized")
    if recipe is None:
        raise HTTPException(status_code=404,detail="recipe not found")

    return {"recipe":recipe}


@app.put("/recipe/{recipe_id}")
async def update_recipe(recipe_id:int,updated:UpdateRecipe,session:SessionDep,current_user:User=Depends(get_current_user)):
    recipe=session.get(Recipe,recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404,detail="recipe not found")
    if recipe.owner_id !=current_user.user_id:
        raise HTTPException(401,"unauthorized")
    recipe.title=updated.title
    recipe.description=updated.description
    recipe.ingredients=updated.ingredients
    recipe.instructions=updated.instructions
    recipe.cook_time=updated.cook_time
    recipe.category=updated.category
    session.commit()
    session.refresh(recipe)

    return {"updated_recipe":recipe}

@app.delete("/recipe/{recipe_id}")
async def delete_recipe(recipe_id:int,session:SessionDep,current_user:User=Depends(get_current_user)):
    recipe=session.get(Recipe,recipe_id)
    if recipe is None:
        raise HTTPException(404,"recipe not found")

    if recipe.owner_id != current_user.user_id:
        raise HTTPException(401,"unauthorized")
    session.delete(recipe)
    session.commit()

    return {"recipe":"deleted successfully"}



