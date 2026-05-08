# schemas is pydantic 
from pydantic import BaseModel, ConfigDict, Field,  EmailStr
from datetime import datetime

class Userbase(BaseModel):
    username:str
    email:str
    age:int
    weight:float
    height:float
    target_weight:float

class UserCreate(Userbase):
    password:str = Field(min_length=8)

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Weightcreate(BaseModel):
    weight:float
class Weightresponse(BaseModel):
    id:int
    user_id:int
    weight:float
    logged_at:datetime
    model_config= ConfigDict(from_attributes=True)
class calorie_intake(BaseModel):
    food_name:str
    quantity:float
class calorie_response(BaseModel):
    id:int
    user_id:int
    food_name:str
    quantity:float
    calories_kcal:float
    protein_g:float
    carb_g:float
    fats_g:float
    logged_at:datetime
    model_config= ConfigDict(from_attributes=True)
class habit_create(BaseModel):
    habit:str
    description:str
class habit_response(BaseModel):
    id: int
    user_id: int
    habit:str
    description:str
    model_config = ConfigDict(from_attributes=True)
class habit_log_create(BaseModel):
    habit_id: int
    completed: bool
    duration: float
class habit_info(BaseModel):
    id: int
    habit: str
    description: str
    model_config = ConfigDict(from_attributes=True)
class habit_log_response(BaseModel):
    id:int
    user_id:int
    habit:habit_info
    completed:bool
    duration:float
    logged_at:datetime
    model_config= ConfigDict(from_attributes=True)
class UserResponse(Userbase):
    model_config= ConfigDict(from_attributes=True)
    #model config just basically alows pydantic to read the object attributes
    #we created when we use a class
    id:int 
    username:str