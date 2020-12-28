from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3

#https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
#from application.app.folder.file import func_name
from models.User import UserLogon, UserCreateDto, UserOutClean
from DAL.user_dal import user_DAL
from utils.pwd_helper import Pwd_Helper

# configuration
DEBUG = True
ROOT_PATH = "/stattracker/api/v1"

#https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
jwt_config = {
    "SECRET_KEY": "e41f43bcf9af08116d93df5d74f56cfd4b9a39584073a3bf44f216ce729c210a",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30
}

app = FastAPI()

#https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{ROOT_PATH}/users", response_model=List[UserOutClean])
async def get_all_users():
    users = user_DAL.get_all_users()
    if users == None:
        raise HTTPException(status_code=404, detail="No Users")
    return users

@app.get(f"{ROOT_PATH}/users/{{user_id}}", response_model=UserOutClean, response_model_exclude_unset=False)
async def get_user_by_id(user_id: int):
    user = user_DAL.get_user_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post(f'{ROOT_PATH}/users', status_code=201) #201 = created
async def create_user(user: UserCreateDto):
    
    if user.password != user.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        user.password = Pwd_Helper.get_password_hash(user.password)
        user_DAL.add_user(user)
        return None
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail=f"'{user.email}' already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # validate_password = Pwd_Helper.verify_password(userCreate.password, hash_password)
    # print(validate_password)


@app.post(f'{ROOT_PATH}/authenticate')
async def authenticate(userLogon: UserLogon):
    
    user = user_DAL.validate_user(userLogon)
    if user:
        return user
    raise HTTPException(status_code=401, detail=f"Logon failed")


    # if not request.json or requestJsonPropInvalid(request, 'userId') or requestJsonPropInvalid(request, 'email') or requestJsonPropInvalid(request, 'password'): 
    #     return ResponseHandler(errorMessage = "Something went wrong, please try again.").jsonify()

    # user = DAL_user.validate_user(userId=request.json['userId'], email=request.json['email'], password=request.json['password'])
    # if user:
    #     del user["password"]        
    #     # Create Token
    #     # Until Then
    #     return ResponseHandler(user).jsonify()
    # else:
    #     return ResponseHandler(errorMessage = "Incorrect username or password").jsonify()    