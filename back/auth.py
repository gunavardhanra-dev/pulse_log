from datetime import datetime, timezone, timedelta# JWT tokens expire you need datetime
#to set when the datetime of the tokens and when they expire
from jose import JWTError, jwt#used to create and decode the tokens, jwt does the encoding and jwt error thrown
#when a token is invalid 
from dotenv import load_dotenv#this is required for hiding the things which need to be hd
import os
from sqlalchemy import select
from sqlalchemy.orm import Session
from back.database import get_db
import back.models as models
from fastapi import Depends,HTTPException, status#depends for dependecny injection 
from fastapi.security import OAuth2PasswordBearer#looks for incoming requests finds the authorization header
#and extracts the token from it ypu point it at your url login 

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
#when you create or when you verify a token it gets signed with this so if soemone tampers with the token 
# the token signature wont match with this secret key and its gets invalidated
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")#the bouncer at the door who checks for the token
#token extractor points us at  the login endpoint 
ALGORITHM="HS256"#signing algo
ACCESS_TOKEN_EXPIRE_MINUTES=30#how long the token is valid for 


#function which creates a jwt token
def create_access_token(data:dict):#takes a dictionary as a parameter
    copied_data= data.copy()#copying the data so that you dont modify the original users data
    expiry= datetime.now(timezone.utc)+ timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    #sets the expiry time current time plus 30 min
    copied_data.update({"exp":expiry})#adds the expry time to the token data
    encoded_jwt= jwt.encode(copied_data, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
"""Omg wait its pretty simple
So jwt.encode creates the actual token we have to use
And to create a jwt token we need the data of the user which also contains the users id
The secret key
And also to the users data dictionary we add the expiry which we have set
And we add the algorithm we are using to sign the token """
#A FUNCTION WHICH VERIFIES THE ACESSS TOKEN
def verify_access_token(token: str,credentials_exceptions):
    try:
        payload =jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id: str =payload.get("sub")#so basically the decode line returns a dict and it conatins the user id
        #stores the user id as "subject" "who is this token about".
        if not user_id:
            raise credentials_exceptions
        return user_id
    except JWTError:
        raise credentials_exceptions  
#its simple we are just decoding and checkng the user exists or to  be  precise there is a user id with the token
# A function to get the current user
def get_currentr_user(token:str =Depends(oauth2_scheme), db:Session =Depends(get_db)):
    #we use a dependdecany injection to automaatically extract the token from the request header is bascially rhe bouncer
    credentials_exceptions= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id= verify_access_token(token,credentials_exceptions)
    result = db.execute(select(models.User). where(models.User.id== user_id))
    user = result.scalars().first()
    return user