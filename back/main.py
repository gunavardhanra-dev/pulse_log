from typing import Annotated
from fastapi import FastAPI,Request,status, Depends, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import os
import requests
import back.models as models
from back.schemas import Userbase,UserCreate,UserResponse,UserLogin, Token, Weightcreate, Weightresponse,calorie_response,calorie_intake,habit_create,habit_response,habit_log_response,habit_log_create
from back.database import Base,get_db, engine
from sqlalchemy.orm import Session
from  sqlalchemy import select
from back.auth import create_access_token, get_currentr_user
app= FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    )


models.Base.metadata.create_all(bind=engine)
pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
#cryptcontext is thr tool from passlib that handles password hashing
#schemes line is the industry standard used for password hashing
#deprecated line is the thing used to make sure if we ever switch algos  handles # schemes

@app.post("/registration", response_model= UserResponse)
def user_registration (user:UserCreate, db:Annotated[Session,Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username==user.username)
    )
    existing_user= result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="the username already exists",
        )
    hashed_password=pwd_context.hash(user.password)
    new_user= models.User(
        username=user.username,
        email=user.email,
        age= user.age,
        weight= user.weight,
        target_weight= user.target_weight,
        height= user.height,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
@app.post("/login",response_model=Token)
def user_login(user:UserLogin,db:Annotated[Session,Depends(get_db)]):
    result= db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="there is not account assocoaited with this mail",
        ) 
    if not pwd_context.verify(user.password, existing_user.password):#verify just checks if
        #the passwords match by taking both orginal passwords and then hasing them
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong password",
        )
    access_token = create_access_token(data= {"sub":str(existing_user.id)})#this is where we define the sub  and we are creating an access token for it and also JWT expects a string not an int
    return {"access_token": access_token,"token_type":"bearer"}

@app.get("/me",response_model=UserResponse)
def get_user(current_user= Depends(get_currentr_user)):
    return current_user

@app.post("/weight", response_model=Weightresponse)
def weight_create(user:Weightcreate, db:Annotated[Session, Depends(get_db)], current_user=Depends(get_currentr_user)):
    new_weight=models.Weight_Log(
        weight=user.weight,
        user_id=current_user.id,
    )
    db.add(new_weight)
    db.commit()
    db.refresh(new_weight)
    return new_weight

@app.get("/weight", response_model=list[Weightresponse])
def weight_respond(db:Annotated[Session,Depends(get_db)],current_user= Depends(get_currentr_user)):
    result= db.execute(
        select(models.Weight_Log).where(models.Weight_Log.user_id==current_user.id)
    )
    weights= result.scalars().all()
    return weights

@app.post("/calorielog", response_model=calorie_response)
def calories_intake(food:calorie_intake ,db:Annotated[Session, Depends(get_db)],current_user=Depends(get_currentr_user)):
    api_key=os.getenv("api_key")#this is the api key we use
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
    params={
        "query":food.food_name,
        "api_key":api_key,
        "pageSize":1
    }
    response= requests.get(url, params=params)
    data=response.json()# we get the data in form of  json with many other values
    food_data= data["foods"][0]
    if not food_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the food requested does not exist"
        )
    nutrients= food_data["foodNutrients"]
    calories = next((n["value"] for n in nutrients if n["nutrientName"] == "Energy"), 0)    
    protein = next((n["value"] for n in nutrients if n["nutrientName"] == "Protein"), 0)
    carbs = next((n["value"] for n in nutrients if n["nutrientName"] == "Carbohydrate, by difference"), 0)
    fats = next((n["value"] for n in nutrients if n["nutrientName"] == "Total lipid (fat)"), 0)
    quantity_ratio=food.quantity/100#we need this becasue usda api gives nutrition values in terms of 

    log_user= models.meal_log(
        user_id=current_user.id,
        food_name=food_data["description"],
        quantity=food.quantity,
        calories_kcal=round(calories*quantity_ratio,2),
        protein_g=round(protein*quantity_ratio,2),
        carb_g=round(carbs*quantity_ratio,2),
        fats_g=round(fats*quantity_ratio,2),
    )

    db.add(log_user)
    db.commit()
    db.refresh(log_user)
    return log_user
@app.get("/calorielog",response_model=List[calorie_response])
def get_calorie(db:Annotated[Session,Depends(get_db)],current_user=Depends(get_currentr_user)):
    result = db.execute(
        select(models.meal_log).where(models.meal_log.user_id==current_user.id)
    )
    calories= result.scalars().all()
    return calories
@app.post("/habit",response_model=habit_response)
def Habit_create(users:habit_create,db:Annotated[Session,Depends(get_db)],current_user=Depends(get_currentr_user)):
    new_habit=models.habit_create(
        habit=users.habit,
        description=users.description,
        user_id=current_user.id,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit
@app.post("/habit/log",response_model=habit_log_response)
def habit_logging(users:habit_log_create,db:Annotated[Session,Depends(get_db)],current_user= Depends(get_currentr_user)):
    new_log=models.habit_log(
        habit_id=users.habit_id,
        completed=users.completed,
        duration=users.duration,
        user_id=current_user.id,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
@app.get("/habit/log", response_model=List[habit_log_response])
def habit_getting(db:Annotated[Session,Depends(get_db)],current_user= Depends(get_currentr_user)):
    result=db.execute(
        select(models.habit_log).where(models.habit_log.user_id==current_user.id)
    )
    habits= result.scalars().all()
    return habits
@app.get("/bmi")
def get_bmi(current_user=Depends(get_currentr_user)):
    height_m = current_user.height / 100 
    bmi = current_user.weight / (height_m ** 2)
    category = "Underweight" if bmi < 18.5 else "Normal" if bmi <= 24.9 else "Overweight"
    return {"bmi": round(bmi, 2), "category": category}

